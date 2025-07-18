from datetime import timedelta, datetime, UTC
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from . import user_crud, user_schema
from .user_crud import pwd_context
from pydantic import ValidationError
from ...models import User
from fastapi.responses import RedirectResponse, JSONResponse
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# from .user_auth import ALGORITHM, REFRESH_KEY_NAME, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, set_cookie, delete_cookie, api_bearer_token
from .._auth.auth import api_bearer_token
from ...database import get_db
from .._comm import comm_crud, comm_schema

router = APIRouter(
    # allow_origins=["*"],
    prefix="/api/web/users",
    tags=["web 공통 users"],
    # dependencies=[Depends(check_domain_auth)],
)


@router.post("/list")
def user_list( 
        item:comm_schema.CommFilterList,
        db: Session = Depends(get_db), 
        api_key: str = Security(api_bearer_token) 
    ):
    user = user_crud.get_user(db, api_key['sub'])
    
    if user.permission != 'super':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="접근 권한이 없습니다")

    page, size, filter= item
    page= page[1]
    size= size[1]
    filter= filter[1]
    filters= eval(filter)

    # print('user-list', api_key['sub'])
    total, list = comm_crud.get_list(
        User, db, skip=page*size, limit=size, filter=filters)
    return {
        'total': total,
        'list': list
    }