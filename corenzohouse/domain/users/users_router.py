from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from ...database import get_db
from ...domain.users import users_crud, users_schema
from ...domain.users.users_crud import pwd_context
from pydantic import ValidationError
from ...model.users import Users


from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from ...domain.users.users_auth import ALGORITHM, REFRESH_KEY_NAME, REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, set_cookie, delete_cookie, api_bearer_token

from ...domain._comm import comm_crud, comm_schema

router = APIRouter(
    prefix="/api/user",
    tags=["corenzo users"]
)
# print(oauth2_scheme.__dir__())

""" @router.post("/create-admin",
)
def users_create_admin(_users_create: users_schema.UserCreatePW, db: Session = Depends(get_db)):
    user = users_crud.get_existing_user(db, users_create=_users_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    return users_crud.create_users_admin(db=db, users_create=_users_create)
 
@router.post("/create-pw", 
            #  status_code=status.HTTP_204_NO_CONTENT
             )
def users_create_pw(_users_create: users_schema.UserCreatePW, db: Session = Depends(get_db)):
    user = users_crud.get_existing_user(db, users_create=_users_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    return users_crud.create_users_pw(db=db, users_create=_users_create)


@router.post("/create", 
            #  status_code=status.HTTP_204_NO_CONTENT
             )
def users_create(_users_create: users_schema.UserCreate, db: Session = Depends(get_db)):
    user = users_crud.get_existing_user(db, users_create=_users_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    return users_crud.create_user(db=db, users_create=_users_create)

@router.put("/update/{id}")
def category_update(
    # item,
    id: int,
    item: users_schema.UserUpdate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token)
):  
    update_data = item.model_dump(exclude_unset=True)
    return users_crud.update_user(db, update_data, id=id)

@router.post("/sns-login", 
            #  response_model=users_schema.Token
             )
def sns_login_for_access_token(response: Response,
                           id: users_schema.User,
                           db: Session = Depends(get_db),
                        ):
    # print(id)
    user = users_crud.get_user(db, id.userid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect userid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token= create_access_token(subject= user.userid)
    refresh_token= create_refresh_token(subject= user.userid)

    set_cookie(response, key=REFRESH_KEY_NAME, value=refresh_token, exp_min= ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userid": user.userid
    }


@router.post("/login", response_model=users_schema.Token)
def login_for_access_token(response: Response,
                           db: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends() ):

    # check user and password
    user = users_crud.get_user(db, form_data.username)
    # print(user.password, pwd_context.hash(form_data.password))
    
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect userid or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token= create_access_token(subject= user.userid)
    refresh_token= create_refresh_token(subject= user.userid)
    
    set_cookie(response, key=REFRESH_KEY_NAME, value=refresh_token, exp_min= ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userid": user.userid
    }


@router.post("/logout")
async def logout (response: Response, request: Request):
    refresh_token= request.cookies.get(REFRESH_KEY_NAME)
    # print(refresh_token)
    delete_cookie(response=response, key=REFRESH_KEY_NAME)
    return HTTPException(status_code=status.HTTP_200_OK, detail='Logout successful')


@router.post("/refresh", response_model=users_schema.Token )
async def refresh (response: Response, request: Request):
    refresh_token= request.cookies.get(REFRESH_KEY_NAME)

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
    

@router.post("/token", 
            #  dependencies=[Depends(api_token)]
             )
def token(api_key: str = Security(api_bearer_token)):
    return api_key

@router.post("/authorization")
def authorization():
    # api_token()
    return


@router.post("/list")
def users_list( 
        item:comm_schema.CommFilterList,
        db: Session = Depends(get_db), 
        api_key: str = Security(api_bearer_token) 
    ):
    user = users_crud.get_user(db, api_key['sub'])
    
    if user.permission != 'super':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="접근 권한이 없습니다")

    page, size, filter= item
    page= page[1]
    size= size[1]
    filter= filter[1]
    filters= eval(filter)

    print('user-list', api_key['sub'])
    total, list = comm_crud.get_list(
        User, db, skip=page*size, limit=size, filter=filters)
    return {
        'total': total,
        'list': list
    }
    
    # return api_key """