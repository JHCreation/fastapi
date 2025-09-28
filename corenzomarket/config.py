import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import importlib

project_name = "corenzomarket"
BASE_DIR= Path(__file__).resolve().parent.parent #루트 폴더
ROOT_DIR= Path(__file__).resolve().parent #현재 프로젝트의 루트 폴더
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# def load_models(basedir):
#     for subdir in Path(basedir).iterdir():
#         if subdir.is_dir() and not subdir.name.startswith("__"):
#             for file_path in subdir.glob("*.py"):
#                 if file_path.is_file():
#                     relative_path = subdir.relative_to(BASE_DIR)
#                     module_base = relative_path.as_posix().replace("/", ".")
#                     module_name= f"{module_base}.{file_path.stem}"
#                     # logger.debug(f'순회중 파일: {relative_path}, {file_path.stem}, {module_name}')
#                     try:
#                         importlib.import_module(module_name)
#                     except Exception as e:
#                         print(f"❌ Error importing models {module_name}: {e}")


logger.debug(f"website cors-origin : {os.getenv("CORS_ORIGIN")}")
