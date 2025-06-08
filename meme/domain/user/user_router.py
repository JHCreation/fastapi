from datetime import timedelta, datetime, UTC
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from meme.database import get_db
from meme.domain.user import user_crud, user_schema
from meme.domain.user.user_crud import pwd_context
from pydantic import ValidationError
from meme.models import User
from fastapi.responses import RedirectResponse, JSONResponse
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from meme.domain.user.user_auth import ALGORITHM, REFRESH_KEY_NAME, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, set_cookie, delete_cookie, api_bearer_token

from meme.domain._comm import comm_crud, comm_schema

router = APIRouter(
    prefix="/api/user",
    tags=["meme users"]
)

# @router.get("/test-set-cookie")
# async def setCookie (response: Response):
#     print('setc', timedelta(minutes=0.084))
#     response.set_cookie(
#         key=REFRESH_KEY_NAME, 
#         value='12345', 
#         expires=datetime.now(UTC) + timedelta(seconds=7), 
#         samesite="none",
#         secure=True,
#         httponly=True
#     )

# @router.get("/test-del-cookie")
# def setCookie (response: Response):
#     response.delete_cookie(
#         key=REFRESH_KEY_NAME, 
#         samesite="none",
#         secure=True,
#         httponly=True
#     )

@router.post("/refresh-token")
def refresh(
    refresh_token: str
):
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
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token= create_access_token(subject= payload.get('sub'))
        return {
            "access_token": access_token,
            # "refresh_token": refresh_token,
            "token_type": "bearer",
            "userid": payload.get('sub')
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


# @router.post("/refresh-bridge")
# def refresh_bridge(
#     response: Response, 
#     request: Request,
#     redirect_uri: str = Form(...),
#     callback_uri: str = Form(...) 
# ):
#     # response = JSONResponse(content={"message": "logged out"})

#     refresh_token= request.cookies.get(REFRESH_KEY_NAME)
#     if type(refresh_token) == type(None):
#         return RedirectResponse(f"{callback_uri}?error=empty&redirect_uri={redirect_uri}", status_code=302)
    
#     try:
#         payload = jwt.decode(
#             refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
#         )
#         if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
#             res= RedirectResponse(f"{callback_uri}?error=token_expired&redirect_uri={redirect_uri}", status_code=302)
#             delete_cookie(response=res, key=REFRESH_KEY_NAME)
#             return res
            

#         access_token= create_access_token(subject= payload.get('sub'))
#         return RedirectResponse(f"{callback_uri}?access_token={access_token}&redirect_uri={redirect_uri}&token_type=bearer&userid={payload.get('sub')}", status_code=302)
    
#     except jwt.ExpiredSignatureError:
#         res= RedirectResponse(f"{callback_uri}?error=token_expired&redirect_uri={redirect_uri}", status_code=302)
#         delete_cookie(response=res, key=REFRESH_KEY_NAME)
#         return res

#     except(jwt.JWTError, ValidationError):
#         res= RedirectResponse(f"{callback_uri}?error=invalid_credentials&redirect_uri={redirect_uri}", status_code=302)
#         delete_cookie(response=response, key=REFRESH_KEY_NAME)
#         return res


# @router.post("/login-bridge")
# def login_bridge(
#         response: Response,
#         db: Session = Depends(get_db),
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         redirect_uri: str = Form(...),
#         callback_uri: str = Form(...) 
#     ):
#     # check user and password
#     user = user_crud.get_user(db, form_data.username)
#     # print(user.password, pwd_context.hash(form_data.password))
    
#     if not user or not pwd_context.verify(form_data.password, user.password):
#         return RedirectResponse(f"{callback_uri}?error=invalid_credentials", status_code=302)

#     access_token= create_access_token(subject= user.userid)
#     refresh_token= create_refresh_token(subject= user.userid)

#     # res= RedirectResponse(f"{callback_uri}?access_token={access_token}&redirect_uri={redirect_uri}", status_code=302)
#     # set_cookie(response=res, key=REFRESH_KEY_NAME, value=refresh_token, exp_min=REFRESH_TOKEN_EXPIRE_MINUTES)
#     # return res

    
#     return RedirectResponse(f"{callback_uri}?access_token={access_token}&redirect_uri={redirect_uri}&refresh_token={refresh_token}", status_code=302)

#     # return {
#     #     "access_token": access_token,
#     #     "token_type": "bearer",
#     #     "userid": user.userid
#     # }


@router.post("/create-admin",
)
def user_create_admin(_user_create: user_schema.UserCreatePW, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    return user_crud.create_user_admin(db=db, user_create=_user_create)
 
@router.post("/create-pw", 
            #  status_code=status.HTTP_204_NO_CONTENT
             )
def user_create_pw(_user_create: user_schema.UserCreatePW, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    return user_crud.create_user_pw(db=db, user_create=_user_create)


@router.post("/create", 
            #  status_code=status.HTTP_204_NO_CONTENT
             )
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    return user_crud.create_user(db=db, user_create=_user_create)

@router.put("/update/{id}")
def category_update(
    # item,
    id: int,
    item: user_schema.UserUpdate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token)
):  
    update_data = item.model_dump(exclude_unset=True)
    return user_crud.update_user(db, update_data, id=id)

@router.post("/sns-login", 
            #  response_model=user_schema.Token
             )
def sns_login_for_access_token(response: Response,
                           id: user_schema.User,
                           db: Session = Depends(get_db),
                        ):
    user = user_crud.get_user(db, id.userid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect userid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token= create_access_token(subject= user.userid)
    refresh_token= create_refresh_token(subject= user.userid)

    set_cookie(response, key=REFRESH_KEY_NAME, value=refresh_token, exp_min=REFRESH_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userid": user.userid
    }


@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(response: Response,
                           db: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends() ):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    # print(user.password, pwd_context.hash(form_data.password))
    
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect userid or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token= create_access_token(subject= user.userid)
    refresh_token= create_refresh_token(subject= user.userid)
    
    # set_cookie(response, key=REFRESH_KEY_NAME, value=refresh_token, exp_min=REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userid": user.userid,
        "refresh_token": refresh_token,
    }


# @router.post("/logout")
# async def logout (response: Response, request: Request):
#     refresh_token= request.cookies.get(REFRESH_KEY_NAME)
#     delete_cookie(response=response, key=REFRESH_KEY_NAME)
#     return HTTPException(status_code=status.HTTP_200_OK, detail='Logout successful')


@router.post("/refresh", response_model=user_schema.Token )
async def refresh (response: Response, request: Request, item: user_schema.RefreshToken):
    refresh_token= item.refresh_token
    # refresh_token= request.cookies.get(REFRESH_KEY_NAME)

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
        print(datetime.fromtimestamp(payload.get('exp')), datetime.now())
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token= create_access_token(subject= payload.get('sub'))
        return {
            "access_token": access_token,
            # "refresh_token": refresh_token,
            "token_type": "bearer",
            "userid": payload.get('sub')
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