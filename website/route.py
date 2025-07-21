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

# def load_domain_routers(
#     basedir, 
#     suffix: str = "_router",
#     attr_name: str = "router"
# ) -> List[APIRouter]:
#     routers = []
#     for subdir in Path(basedir).iterdir():
#         if subdir.is_dir() and not subdir.name.startswith("__"):
#             router_filename = f"{subdir.name}{suffix}.py"
#             router_path = subdir / router_filename

#             if router_path.exists():
#                 relative_path = subdir.relative_to(BASE_DIR)
#                 module_base = relative_path.as_posix().replace("/", ".")
#                 # print('router_path', relative_path, module_base, subdir.name)
#                 module_name= f"{module_base}.{subdir.name}{suffix}"
#                 try:
#                     module = importlib.import_module(module_name)
#                     router = getattr(module, attr_name, None)
#                     if isinstance(router, APIRouter):
#                         routers.append(router)
#                     else:
#                         logger.warning(f"⚠️ {module_name}에 '{attr_name}' 속성이 없거나 APIRouter가 아닙니다.")
#                 except Exception as e:
#                     logger.error(f"❌ Error importing {module_name}: {e}")

#     return routers

routers= load_domain_routers(ROOT_DIR / "domain", "_router")
origins = os.environ.get('CORS_ORIGIN').split(',') if os.environ.get('CORS_ORIGIN') else []
website_app = FastAPI(
    swagger_ui_parameters={
        "docExpansion": "none",
    }
)
website_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in routers:
    website_app.include_router(route)

app.mount("/api/web", website_app)
