import os
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import importlib
from pathlib import Path
from typing import List
from .config import BASE_DIR, ROOT_DIR, logger
from main import app
import json
import sys

def load_domain_routers(
    basedir: Path, 
    suffix: str = "_route", 
    attr_name: str = "router" 
):
    routers = []

    for subdir in Path(basedir).iterdir():
        if not subdir.is_dir() or subdir.name.startswith("__"):
            continue

        for file in subdir.iterdir():
            if file.is_file() and file.name.endswith(f"{suffix}.py"):
                # 모듈 경로를 계산
                relative_path = file.relative_to(Path.cwd()).with_suffix("")  # .py 제거
                module_path = relative_path.as_posix().replace("/", ".")
                
                try:
                    module = importlib.import_module(module_path)
                    router = getattr(module, attr_name, None)
                    if isinstance(router, APIRouter):
                        routers.append(router)
                except Exception as e:
                    print(f"❌ Error importing {module_path}: {e}")

    return routers

routers= load_domain_routers(ROOT_DIR / "domain", "_router")
origins = os.environ.get('CORS_ORIGIN').split(',') if os.environ.get('CORS_ORIGIN') else []
project_app = FastAPI(
    swagger_ui_parameters={
        "docExpansion": "none",
    }
)
project_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in routers:
    project_app.include_router(route)

app.mount("/corenzomarket", project_app)
