import os
import json
from dotenv import load_dotenv
# from config import ROOT_DIR
current_file_path = os.path.abspath(__file__)
ROOT_DIR=os.path.dirname(current_file_path)


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Response, Request


def get_allowed_origins(origin):
    print(origin)
    if origin.endswith(".example.com"):
        return [origin]
    return []

app = FastAPI()
import corenzohouse.route
import meme.route
import website.route
import corenzomarket.route
# 얘네들이 실행되면서 load_dotenv(override)도 같이 덮어버리니 주의(순서)!

load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": (await request.body()).decode()},
    )

if __name__ == 'main':
    origins = json.loads(os.environ.get('CORS_ORIGIN'))
    # app.add_middleware(
    #     CORSMiddleware,
    #     # allow_origins=[],
    #     allow_origins=origins,
    #     # allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    #     # allow_origin_func=get_allowed_origins,
    # )
    





# # 모든 출처를 허용하는 서브 앱
# sub_app_all_origins = FastAPI()
# sub_app_all_origins.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # 특정 출처만 허용하는 서브 앱
# sub_app_specific_origins = FastAPI()
# sub_app_specific_origins.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://my-frontend.com"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @sub_app_specific_origins.get("/private")
# async def read_private():
#     return {"message": "Private access allowed only from my-frontend.com"}

# # 메인 앱에 서브 앱들을 포함시킵니다.
# app.mount("/api/public", sub_app_all_origins)
# app.mount("/api/private", sub_app_specific_origins)

# # 메인 앱 자체의 CORS 설정 (필요하다면)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8000"], # 기본적으로 메인 앱은 localhost만 허용
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )