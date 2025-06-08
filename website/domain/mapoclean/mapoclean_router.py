from ...route import load_domain_routers
from pathlib import Path
from main import app

from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security

ALLOWED_ORIGINS = ["http://localhost:5173", "example.com"]
async def check_domain_auth(request: Request):
    print('마포크린 요청 호스트 검사', request.headers.get("origin"))
    if request.headers.get("origin") not in ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail="Not authorized")

router = APIRouter(
    # allow_origins=["*"],
    prefix="/api/web/mapoclean",
    tags=["mapo-clean"],
    # dependencies=[Depends(check_domain_auth)],
)

routers= load_domain_routers(f"{Path(__file__).resolve().parent}", "_router")
for route in routers:
    router.include_router(route)
