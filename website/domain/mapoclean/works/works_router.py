from datetime import timedelta, datetime, UTC
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from ..mapoclean_router import router

from ....database import get_db
router = APIRouter(
    prefix="/works",
    # tags=["mapoclean/works"]
)

@router.get("/test")
def test():
    return [
        { 
            'title': 'test-title',
            'subject': '마포크린 제목입니다.'
        }
    ]