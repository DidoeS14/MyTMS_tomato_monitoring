import datetime
import os

from ultralytics import YOLO

from chart import draw_chart
from database import writer, Disease, Growth
from config import tomato_model_config
from ftp import ftp_config, ftp_server


class Detector:
    """
    A class for running YOLO-based object detection and analyzing results for tomato plant-related images.<br>
    :param
    Argumets:
    weights (str): Path to the YOLO model weights.
            model (YOLO): YOLO model instance initialized with the specified weights.
            class_names (list): Names of the classes recognized by the YOLO model.
            results (list): Results from the YOLO model for the current run.
            confidences (list): A list of confidence values for detected objects in the current run.
            counts (list): A list of counts of detected object classes for each image in the current run.
    """

    def __init__(self, weights_path: str):
        """
                Initializes the Detector class with the given weights path.

                Args:
                    weights_path (str): Path to the YOLO model weights.
        """
        self.weights = weights_path
        self.model = YOLO(self.weights)
        self.results = None

    def run(self, input_: str):
        """
        Runs the YOLO model on the input data. Note: Grab .results to get the results from the detection
        :arg input_: Path to the input source, being image, folder with images, video or stream
        """
        if self.results is not None:
            self.results = None
        self.results = self.model(input_)


class Analyzer:
    """
    Has function for analyzation the results from the detector
    """

    def __init__(self, results, model):
        self.model = model
        self.class_names = self.model.names
        self.results = results
        self.confidences = []  # gathers all confidences from the current run
        self.counts = []  # gathers all counts from current run ( for each image)

    def analyze_results(self, identification_name: str = None, save_path: str = None, draw_charts: bool = True):
        """
        Analyzes the detection results to compute counts and confidences for each class.

        :param identification_name: (optional) it is typically used to identify the images if they are going to be saved. Usually frame index plus model purpose is a good option!
        :param save_path: (optional) Directory to save annotated images and charts. Defaults to None. If not provided
        then no file will be saved
        :param draw_charts: (optional) Whether to draw and save charts for object counts. Defaults to True.
        :return:
        """

        if save_path is not None:
            os.makedirs(save_path, exist_ok=True)

        for i, result in enumerate(self.results):
            name = os.path.basename(result.path)
            detection_counts = {}

            # Collect unique confidences
            detection_confidences = {}

            for box in result.boxes:
                class_index = int(box.cls)
                class_name = self.class_names[class_index]

                # Use confidence as the key and a unique identifier as the value
                confidence_key = box.conf.item()
                unique_value = f'{name}_{class_name}_{i}'

                # Check if confidence key already exists
                if confidence_key not in detection_confidences:
                    detection_confidences[confidence_key] = unique_value

                # Update the detection count for the class
                if class_name in detection_counts:
                    detection_counts[class_name] += 1
                else:
                    detection_counts[class_name] = 1

            # Append a copy of the current detection_confidences to avoid mutation issues
            self.confidences.append(detection_confidences.copy())

            # print(f'Counts: {name} has {detection_counts}')
            # print(f'Confidences: {name} has {detection_confidences}')

            # Store counts for this result
            self.counts.append(detection_counts)

            # Optionally draw charts and save results
            if identification_name is None:
                identification_name = 'unknown'

            filename = f'{identification_name}_{name}'

            if not ftp_config.use_ftp:
                if draw_charts:
                    draw_chart(data=detection_counts, image=filename, save_path=save_path)
                if save_path is not None:
                    if tomato_model_config.save_images:
                        print(f'Saved image at {save_path}/{filename}')
                        result.save(f'{save_path}/{filename}')
            else:
                ftp_server.connect()
                ftp_server.send_image_data_from_result(result,filename)
                ftp_server.ftp.quit()

    def is_any_confidence_more_than(self, min_threshold):
        return any(float(value) > min_threshold for d in self.confidences for value in d.keys())

    def is_any_confidence_less_than(self, max_threshold):
        return any(float(value) < max_threshold for d in self.confidences for value in d.keys())

    def is_any_count_more_than(self, min_threshold):
        return any(float(value) > min_threshold for d in self.counts for value in d.values())

    def is_any_count_less_than(self, max_threshold):
        return any(float(value) < max_threshold for d in self.counts for value in d.values())

    def check_for_illness(self, confidence):
        is_ill = self.is_any_confidence_more_than(confidence)
        illness_detected = self.is_any_count_more_than(0)

        if illness_detected and is_ill:
            update.for_disease(self.counts)
            return True
        else:
            return False

    def check_for_ready_tomatoes(self, min_size_confidence, min_count):
        """
        Checks for ready tomatoes based on confidence threshold and ripeness level.

        :param min_size_confidence: Confidence threshold to qualify as "ready."
        :return: Number of ready tomatoes or False if none found.
        """
        # TODO: maybe check by area in future
        # Check if there are fully ripened tomatoes in the counts
        if self.is_any_count_more_than(min_count):
            # Use the is_any_confidence_more_than method to check if any confidence is above the threshold
            ready_count = 0

            for conf_dict in self.confidences:
                for confidence, description in conf_dict.items():
                    # Check if the confidence exceeds the threshold and if it's related to a fully ripened tomato
                    if confidence > min_size_confidence and 'fully' in description:
                        ready_count += 1

            return ready_count if ready_count > 0 else False

        return False

    def estimate_next_ready_tomatoes(self):
        # TODO: for more exact calculations can be used temperature data
        half_ripened_count = [value for detection in self.counts for key, value in detection.items() if 'half' in key]
        five_days_date = datetime.datetime.now().date() + datetime.timedelta(days=5)
        seven_days_date = datetime.datetime.now().date() + datetime.timedelta(days=7)
        message = f'{sum(half_ripened_count)} tomatoes are estimated to be ready in 5 to 7 days ' \
                  f'(between {five_days_date} and {seven_days_date})'
        print(message)


class Update:
    """
    Updates database by queries
    """

    def __init__(self):
        pass

    def for_disease(self, detected: list):
        """
        Writes data for the detected disease in the database
        :param detected: A list with all dictionaries in format {illness: count}
        :return:
        """
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        area = 'unidentified'  #TODO: there will be need for area to be taken from another data structure. Maybe
                               # something like {area: {illness: count}}. Also the name of the picture can be the
                               # name of the area for simplicity

        for detection in detected:
            for key, value in detection.items():
                if 'Healthy' in key:
                    continue

                illness = key
                count = value

                writer.add_data(
                    Disease,
                    date=date,
                    area=area,
                    illness=illness,
                    ill_count=count
                )

    def for_tomato_state(self, detected):
        """
        Processes the detected tomato states and writes the accumulated counts for each state (green, half-ripened, fully ripened) into the database.

        This method iterates over the detection results and classifies the tomatoes into three categories based on their ripeness: green, half-ripened, and fully ripened. The counts for each category are accumulated, and the results are written to the database along with the current timestamp and area information.

        The function assumes that the detection result is a list of dictionaries, where each dictionary contains key-value pairs representing tomato states (e.g., 'l_green', 'b_green' for green tomatoes, 'l_half_ripened', 'b_half_ripened' for half-ripened, and 'l_fully_ripened', 'b_fully_ripened' for fully ripened). The values in these keys represent the count of tomatoes in each respective category."""
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        area = 'unidentified'  #TODO: there will be need for area to be taken from another data structure. Maybe
                               # something like {area: {illness: count}}. Also the name of the picture can be the
                               # name of the area for simplicity


        green, half, ready = 0, 0, 0

        for detection in detected:
            for key, value in detection.items():
                if 'Healthy' in key:
                    continue

                # Accumulate counts for each category
                if key == 'l_green' or key == 'b_green':
                    green += value
                elif key == 'l_half_ripened' or key == 'b_half_ripened':
                    half += value
                elif key == 'l_fully_ripened' or key == 'b_fully_ripened':
                    ready += value

        writer.add_data(
            Growth,
            date=date,
            area=area,
            green_count=green,
            half_ripened_count=half,
            fully_ripened_count=ready
        )
        #IMPORTANT: for now it adds all detected tomatoes, regardless of the confidence!


update = Update()
