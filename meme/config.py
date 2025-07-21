import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import importlib

BASE_DIR= Path(__file__).resolve().parent.parent #루트 폴더
ROOT_DIR= Path(__file__).resolve().parent #현재 프로젝트의 루트 폴더
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)