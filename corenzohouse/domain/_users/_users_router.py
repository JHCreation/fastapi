from datetime import timedelta, datetime, UTC
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from fastapi import APIRouter, HTTPException, Request, Depends, Body
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_async_db
from ...config import logger
from .._comm import comm_schema, comm_crud
from ...models import User
from .user_schema import UsersCreate, UsersDeletes, UsersUpdate
from .._auth.auth import api_bearer_token, get_password_hash
from . import user_crud

from ...database import get_db
router = APIRouter(
    prefix="/api/web/users",
    tags=["web 공통 users"]
)

@router.get("/list")
async def list(
    # db: Annotated[AsyncSession, Depends(get_async_db)], 
    db: AsyncSession = Depends(get_async_db),
    params: comm_schema.CommFilterList = Depends(),
):
    logger.debug(params)
    total, list= await comm_crud.async_get_list(User, db, skip=params.skip, limit=params.limit)
    return {
        "total": total,
        "list": list
    }

@router.post("/create")
async def create_works(
    item: UsersCreate,
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):
    # user = user_crud.get_existing_user(db, user_create=item)
    user= await comm_crud.async_get_item(User, db, key="userid", value=item.userid)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    
    hashed_password= get_password_hash(item.password)
    param= item.model_dump(exclude={'password_confirm'}, exclude_unset=True, exclude_none=True)
    param['password']= hashed_password
    # logger.debug(f'{user}, {hashed_password}, {param}')
    # return
    update= {
        'create_date' : datetime.now(),
        'modify_date' : datetime.now(),
    }
    return await comm_crud.async_create(User, db, param, res_id='id', update=update)

@router.put("/update/{id}")
async def update_works(
    id: str,
    # params: CategorysBase,
    db: AsyncSession = Depends(get_async_db),
    item: UsersUpdate = Body(...),
    api_key: str = Security(api_bearer_token)
):
    param= item
    if item.password:
        param= item.model_dump(exclude={'password_confirm'}, exclude_unset=True, exclude_none=True)
        hashed_password= get_password_hash(item.password)
        param['password']= hashed_password
    update= {
        'modify_date' : datetime.now(),
    }
    return await comm_crud.async_update(User, db, param, filter_key='id', filter_value=id, res_id='id', update=update)

@router.delete("/deletes")
async def works_deletes(
    param: UsersDeletes,
    # ids: List[int]= Query(...),
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Security(api_bearer_token)
):
    return await comm_crud.async_deletes(User, db, filter_key='userid', filter_value=param.ids)