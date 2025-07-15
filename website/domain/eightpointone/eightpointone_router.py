import os
from ...route import load_domain_routers
from pathlib import Path
from main import app

from fastapi import HTTPException, Request
from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends, Security
from dotenv import load_dotenv
load_dotenv()

EMAIL_ACCOUNT= os.environ.get('EMAIL_ACCOUNT_EPO')
EMAIL_PASSWORD= os.environ.get('EMAIL_PASSWORD_EPO')
EMAIL_TO= os.environ.get('EMAIL_TO_EPO')

DOMAIN_NAME="eightpointone"
DOMAIN_ROOT="https://epo.kr"
DOMAIN_WWW="https://www.epo.kr"
ALLOWED_ORIGINS = ["http://localhost:5173", DOMAIN_ROOT, DOMAIN_WWW]

async def check_domain_auth(request: Request):
    print('마포크린 요청 호스트 검사', request.headers.get("origin"))
    if request.headers.get("origin") not in ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail="Not authorized")

router = APIRouter(
    prefix="/api/web/eightpointone",
    tags=["epo"],
    # dependencies=[Depends(check_domain_auth)],
)

routers= load_domain_routers(f"{Path(__file__).resolve().parent}", "_router")
for route in routers:
    router.include_router(route)
