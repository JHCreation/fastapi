from .database import Base
from .config import logger

import pkgutil
import importlib
from . import model as _model_pkg

def _auto_import_models():
    for module_info in pkgutil.iter_modules(_model_pkg.__path__):
        name = module_info.name
        if name.startswith("_"):
        # if name.startswith("_") or name in import_order:
            continue
        full_name = f"{_model_pkg.__name__}.{name}"
        logger.debug(f"[models.py] Importing {full_name}")
        try:
            importlib.import_module(full_name)
        except Exception as e:
            logger.debug(f"[models.py] Failed to import {full_name}: {e}")
_auto_import_models()

