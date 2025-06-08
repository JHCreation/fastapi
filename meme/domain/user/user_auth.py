import os
from datetime import timedelta, datetime, timezone, UTC

from fastapi import  HTTPException, Response, Request
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader, HTTPBearer, OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from meme.database import get_db
from meme.domain.user import user_crud, user_schema
from meme.domain.user.user_crud import pwd_context
from typing import Union, Any
from pydantic import ValidationError

from ...config import ROOT_DIR
from dotenv import load_dotenv
# load_dotenv()
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)
ACCESS_TOKEN_EXPIRE_MINUTES= float(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES= float(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))
# ACCESS_TOKEN_EXPIRE_MINUTES= 1 #5/60 
# REFRESH_TOKEN_EXPIRE_MINUTES= 30 #20/60 
# print(ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES)
SECRET_KEY= os.environ.get('SECRET_KEY')
REFRESH_SECRET_KEY= os.environ.get('REFRESH_SECRET_KEY')
ALGORITHM= os.environ.get('ALGORITHM')
REFRESH_KEY_NAME= os.environ.get('REFRESH_KEY_NAME')
# print(REFRESH_TOKEN_EXPIRE_MINUTES)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
get_bearer_token = HTTPBearer(auto_error=False)
print('meme SECRET_KEY', SECRET_KEY, ROOT_DIR, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES)
def auth_token(token: str, secret_key: str= SECRET_KEY):
    try:
        payload= jwt.decode(
            token, secret_key, algorithms=[ALGORITHM]
        )
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            # detail="Could not validate credentials",
            detail="인증되지 않았습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

async def api_bearer_token(token: str = Depends(get_bearer_token) ):
    if token is None:
        bearerToken= ''
    else:
        bearerToken= token.credentials
    return auth_token(bearerToken)
    
async def api_token(token: str = Depends(api_key_header) ):
    return auth_token(token)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        expires_delta = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode:user_schema.JWT = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    print(datetime.now(timezone.utc), timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES), expires_delta)
    to_encode:user_schema.JWT = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def set_cookie(response: Response, key: str, value, exp_min):
    expires= datetime.now(UTC) + timedelta(minutes=exp_min)
    response.set_cookie(key=key, 
                        value=value, 
                        # path="/",
                        expires=expires, 
                        samesite="none",
                        secure=True,
                        httponly=True)
    
def delete_cookie(response: Response, key: str):
    print('delete', key)
    response.delete_cookie( key=key,
                            # path="/",
                            samesite="none",
                            secure=True,
                            httponly=True)

    

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db) ):
    payload= auth_token(token)
    user = user_crud.get_user(db, userid= payload.get('sub'))
    # user: Union[dict[str, Any], None] = db.get(token_data.sub, None)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user



# def get_current_user(token: str = Depends(oauth2_scheme),
#                      db: Session = Depends(get_db)):
    
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     else:
#         user = user_crud.get_user(db, username=username)
#         if user is None:
#             raise credentials_exception
#         return user