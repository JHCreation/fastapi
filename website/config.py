import os
import logging
from pathlib import Path
import importlib

BASE_DIR= Path(__file__).resolve().parent.parent #루트 폴더
ROOT_DIR= Path(__file__).resolve().parent #현재 프로젝트의 루트 폴더

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

def load_models(basedir):
    for subdir in Path(basedir).iterdir():
        if subdir.is_dir() and not subdir.name.startswith("__"):
            for file_path in subdir.glob("*.py"):
                if file_path.is_file():
                    relative_path = subdir.relative_to(BASE_DIR)
                    module_base = relative_path.as_posix().replace("/", ".")
                    module_name= f"{module_base}.{file_path.stem}"
                    # logger.debug(f'순회중 파일: {relative_path}, {file_path.stem}, {module_name}')
                    try:
                        importlib.import_module(module_name)
                    except Exception as e:
                        print(f"❌ Error importing models {module_name}: {e}")

