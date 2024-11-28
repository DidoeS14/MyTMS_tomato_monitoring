import os
import datetime

from config import tomato_model_config
from video_processing import VideoProcessor


source = tomato_model_config.source
processor = VideoProcessor(video_source=source, frame_interval=5)

processor.start_processing()
#TODO: maybe make the show picture, save image detections and draw chart be configurable through config.ini
