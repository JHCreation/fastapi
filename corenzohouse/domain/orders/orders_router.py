import os
from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from fastapi import FastAPI, Body
import asyncio

from ...database import get_db, get_async_db
from ...domain.orders import orders_crud, orders_schema
# from orders_schema import Subscription
from pydantic import ValidationError
import json

from corenzohouse.route import router, router2
from corenzohouse.database import get_db, get_async_db
from ...domain._comm import comm_crud

# from _utils.crud import comm_crud

from ...config import ROOT_DIR
from dotenv import load_dotenv
from ...model.orders import Orders
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)


@router.get("/orders", 
            #  status_code=status.HTTP_204_NO_CONTENT
             )
async def orders_get_list(request: Request, db: Session = Depends(get_async_db)):
    total, list = await comm_crud.aync_get_list_all(Orders, db)
    return {
        'total': total,
        'list': list
    }

# Create
@router.post("/orders")
async def subscribe(
    item: orders_schema.OrdersCreate,
    db: Session = Depends(get_async_db),
):
    # 구독 정보를 데이터베이스에 저장하는 로직을 여기에 구현
    update= {
        'modify_date' : datetime.now(),
        'create_date' : datetime.now(),
    }
    return await comm_crud.asyncCreate(Orders, db, item, res_id='id', update=update)

# @router.delete("/orders")
# async def subscribe(
#     item: orders_schema.OrdersDelete,
#     db: Session = Depends(get_async_db),
# ):
#     print(item)
#     return await comm_crud.asyncDelete(Orders, db, filter_key='id', filter_value=item.endpoint, res_id='id')
    