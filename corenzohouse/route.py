# import os
# import json
# # from dotenv import load_dotenv
# # load_dotenv()

# from fastapi import FastAPI, HTTPException, Request
# from starlette.middleware.cors import CORSMiddleware
# from fastapi import APIRouter, HTTPException, Response, Request
# from fastapi import Depends, Security


# # app = FastAPI()

# from main import app
# # print(Request.headers.get("host"))

# # origins = json.loads(os.environ.get('CORS_ORIGIN'))
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     # allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# async def check_domain1_auth(request: Request):
#     print('여기', request.headers.get("host"))
#     if request.headers.get("host") != "127.0.0.1:8000":
#         raise HTTPException(status_code=403, detail="Not authorized")

# async def check_domain2_auth(request: Request):
#     if request.headers.get("host") != "127.0.0.1:8000":
#         raise HTTPException(status_code=403, detail="Not authorized 22")

# router = APIRouter(
#     # allow_origins=["*"],
#     prefix="/corenzo",
#     tags=["corenzohouse"],
#     # dependencies=[Depends(check_domain1_auth)],
# )
# # router.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# router2 = APIRouter(
#     prefix="/corenzohouse2",
#     tags=["corenzohouse2"],
#     dependencies=[Depends(check_domain2_auth)],
# )

# from .domain.users import users_router
# from .domain.webpush import webpush_router
# from .domain.orders import orders_router
# from .domain.order_group import order_group_router
# from .domain.reviewers import reviewers_router

# app.include_router(router)
# app.include_router(users_routers.router)
# app.include_router(user_routers.router2)

















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
corenzo_app = FastAPI(
    swagger_ui_parameters={
        # "defaultModelsExpandDepth": -1,    # 전체 모델 정의 숨김
        # "defaultModelExpandDepth": 0,      # 단일 모델 접기
        "docExpansion": "none",            # 전체 operation collapse ("list", "full", "none")
    }
)
corenzo_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in routers:
    corenzo_app.include_router(route)

app.mount("/api/corenzo", corenzo_app)
