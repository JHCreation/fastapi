import os
import json
# from dotenv import load_dotenv
# load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security


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
    print('여기', request.headers.get("host"))
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

from corenzohouse.domain.user import user_router


app.include_router(user_router.router)
app.include_router(user_router.router2)