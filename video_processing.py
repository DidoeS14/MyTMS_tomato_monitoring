import cv2
import time
from config import tomato_model_config, chart_config
from manager import Detector, Analyzer, notify
from email_manager import email


class VideoProcessor:
    def __init__(self, video_source, frame_interval=5):
        """
        Initializes the VideoProcessor class.

        :param video_source: Path to the video file, video stream link or camera index (e.g., 0 for default webcam).
        :param frame_interval: Time interval (in seconds) between frames to process.
        """
        self.video_source = video_source
        self.frame_interval = frame_interval
        self.cap = cv2.VideoCapture(video_source)
        self.save_frames_path = tomato_model_config.output_folder
        self.draw_chart = chart_config.save

        # Initialize detectors and analyzers
        self.tomato_size_detection = Detector(weights_path=tomato_model_config.size_tomato_model_path)
        self.tomato_disease_detection = Detector(weights_path=tomato_model_config.disease_tomato_model_path)

    def process_frame(self, frame):
        """
        Process a single frame to detect diseases and tomato size.

        :param frame: The video frame to process.
        """
        frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1

        # Run disease detection
        self.tomato_disease_detection.run(input_=frame)
        analyze_for_disease = Analyzer(self.tomato_disease_detection.results, self.tomato_disease_detection.model)
        analyze_for_disease.analyze_results(
            identification_name=f'{frame_index}_disease',
            save_path=self.save_frames_path,
            draw_charts=self.draw_chart)

        # Check for illness
        if analyze_for_disease.check_for_illness(tomato_model_config.disease_tomato_confidence):
            email.send("Disease is detected!")
            return "disease_detected"

        # Run size detection
        self.tomato_size_detection.run(input_=frame)
        analyze_sizes = Analyzer(self.tomato_size_detection.results, self.tomato_size_detection.model)
        analyze_sizes.analyze_results(
            identification_name=f'{frame_index}_size',
            save_path=self.save_frames_path,
            draw_charts=self.draw_chart)

        # Count ready tomatoes
        ready_tomatoes_count = analyze_sizes.check_for_ready_tomatoes(
            tomato_model_config.size_tomato_confidence,
            tomato_model_config.size_tomato_ripened_count)

        if ready_tomatoes_count is not False:
            message = f'There are {ready_tomatoes_count} ready tomatoes to be harvested!'
            print(f'Sending message: {message}')
            email.send(message)

        # Notify the state of the tomatoes
        notify.for_tomato_state(analyze_sizes.counts)
        analyze_sizes.estimate_next_ready_tomatoes()

        return "frame_processed"

    def start_processing(self):
        """
        Start the video processing loop.
        Processes one frame every 'frame_interval' seconds.
        """
        show = tomato_model_config.show_stream
        last_processed_time = time.time()

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame, exiting.")
                break

            current_time = time.time()
            if current_time - last_processed_time >= self.frame_interval:
                print(f"Processing frame at {current_time} seconds...")
                result = self.process_frame(frame)
                if result == "disease_detected":
                    break
                last_processed_time = current_time

            # Optional: Display the frame (for debugging purposes)
            if show:
                cv2.imshow("Video", frame)
                # Check if 'q' is pressed to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Clean up and release resources
        self.cap.release()
        cv2.destroyAllWindows()


