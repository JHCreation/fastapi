import os
import logging

current_file_path = os.path.abspath(__file__)
ROOT_DIR=os.path.dirname(current_file_path)


log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)