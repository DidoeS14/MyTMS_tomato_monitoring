import os
import datetime

from config import tomato_model_config
from manager import Detector, Analyzer, notify
from email_manager import email

tomato_size_detection = Detector(weights_path=tomato_model_config.size_tomato_model_path)
tomato_disease_detection = Detector(weights_path=tomato_model_config.disease_tomato_model_path)

tomato_disease_detection.run(input_=tomato_model_config.input_folder)
analyze_for_disease = Analyzer(tomato_disease_detection.results, tomato_disease_detection.model)
analyze_for_disease.analyze_results()

if analyze_for_disease.check_for_illness(tomato_model_config.disease_tomato_confidence):
    email.send("Disease is detected!")
    exit()  # Temporary exit, for debugging purposes

tomato_size_detection.run(input_=tomato_model_config.input_folder)
analyze_sizes = Analyzer(tomato_size_detection.results, tomato_size_detection.model)
analyze_sizes.analyze_results()

ready_tomatoes_count = analyze_sizes.check_for_ready_tomatoes(
    tomato_model_config.size_tomato_confidence,
    tomato_model_config.size_tomato_ripened_count)

if ready_tomatoes_count is not False:
    message = f'There are {ready_tomatoes_count} ready tomatoes to be harvested!'
    print(f'Sending message: {message}')
    email.send(message)

notify.for_tomato_state(analyze_sizes.counts)
analyze_sizes.estimate_next_ready_tomatoes()

#TODO: proceed with checking size using the model
# if red tomatoes are more than x and their confidence is over 0.8 then send email

