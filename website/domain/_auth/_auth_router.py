from fastapi import APIRouter

from datetime import timedelta, datetime, UTC
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

# from . import user_crud, user_schema
# from .user_crud import pwd_context
from pydantic import ValidationError
from ...models import User
from fastapi.responses import RedirectResponse, JSONResponse
from .auth import verify_password, set_cookie, create_refresh_token, create_access_token, delete_cookie, ALGORITHM, REFRESH_KEY_NAME, REFRESH_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES
from ...config import logger
from .auth_schema import Token, RefreshToken
from ...database import get_db
from .._users import user_crud
router = APIRouter(
    # allow_origins=["*"],
    prefix="/api/web/auth",
    tags=["web 공통 auth"],
    # dependencies=[Depends(check_domain_auth)],
)
@router.post("/login")
def login(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_crud.get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디와 비밀번호를 확인 해주세요.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token= create_access_token({
        'userid': user.userid,
        'usertype': user.usertype,
        'permission': user.permission
    })
    refresh_token= create_refresh_token({
        'userid': user.userid,
        'usertype': user.usertype,
        'permission': user.permission
    })
    
    set_cookie(response, key=REFRESH_KEY_NAME, value=refresh_token, exp_min=REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        # "token_type": "bearer",
        "userid": user.userid,
        "usertype": user.usertype,
        "permission": user.permission,
        "refresh_token": refresh_token,
    }

@router.post("/logout")
async def logout (response: Response, request: Request):
    # refresh_token= request.cookies.get(REFRESH_KEY_NAME)
    delete_cookie(response=response, key=REFRESH_KEY_NAME)
    return HTTPException(status_code=status.HTTP_200_OK, detail='Logout successful')


@router.post("/refresh", response_model=Token )
async def refresh ( response: Response, request: Request ):
    refresh_token= request.cookies.get(REFRESH_KEY_NAME)
    logger.debug(f'key:{REFRESH_KEY_NAME}, refresh:{type(refresh_token)}, None:{type(None)}')
    if type(refresh_token) == type(None):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials(Empty)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(
            refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        # print(datetime.fromtimestamp(payload.get('exp')), datetime.now())
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token= create_access_token({
            'userid': payload.get('userid'),
            'usertype': payload.get('usertype'),
            'permission': payload.get('permission')
        })
        return {
            "access_token": access_token,
            # "refresh_token": refresh_token,
            # "token_type": "bearer",
            # "userid": payload.get('userid')
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )