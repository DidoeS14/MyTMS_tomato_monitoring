
from config import tomato_model_config
from video_processing import VideoProcessor


source = tomato_model_config.source

processor = VideoProcessor(video_source=source, frame_interval=tomato_model_config.cooldown)
processor.start_processing()
