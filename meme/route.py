import os
import json
# from dotenv import load_dotenv
# load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from .config import BASE_DIR, ROOT_DIR, logger





# app = FastAPI()

from main import app
# print(Request.headers.get("host"))

# origins = json.loads(os.environ.get('CORS_ORIGIN'))
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     # allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

async def check_domain1_auth(request: Request):
    print('request.headers.get',request.headers.get("host"))
    if request.headers.get("host") != "127.0.0.1:8000":
        raise HTTPException(status_code=403, detail="Not authorized")

async def check_domain2_auth(request: Request):
    if request.headers.get("host") != "127.0.0.1:8000":
        raise HTTPException(status_code=403, detail="Not authorized 22")

router = APIRouter(
    # allow_origins=["*"],
    prefix="/corenzo",
    tags=["corenzohouse"],
    dependencies=[Depends(check_domain1_auth)],
)
# router.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

router2 = APIRouter(
    prefix="/corenzohouse2",
    tags=["corenzohouse2"],
    dependencies=[Depends(check_domain2_auth)],
)

origins = os.environ.get('CORS_ORIGIN').split(',') if os.environ.get('CORS_ORIGIN') else []
meme_app = FastAPI(
    swagger_ui_parameters={
        # "defaultModelsExpandDepth": -1,    # 전체 모델 정의 숨김
        # "defaultModelExpandDepth": 0,      # 단일 모델 접기
        "docExpansion": "none",            # 전체 operation collapse ("list", "full", "none")
    }
)
print('CORS_ORIGIN meme route!', origins)
meme_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .domain.files import files_router
from .domain.category import category_router
from .domain.campaign import campaign_router
from .domain.question import question_router
from .domain.answer import answer_router
from .domain.user import user_router
from .domain.works import works_router
from .domain.contact import contact_router

meme_app.include_router(files_router.router)
meme_app.include_router(question_router.router)
meme_app.include_router(answer_router.router)
meme_app.include_router(user_router.router)
meme_app.include_router(campaign_router.router)
meme_app.include_router(category_router.router)
meme_app.include_router(works_router.router)
meme_app.include_router(contact_router.router)
app.mount("/myz", meme_app)