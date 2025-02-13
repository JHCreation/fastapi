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

# from orders_crud import order_get_list

@router.get("/orders")
async def orders_get_list(
    request: Request, 
    db: Annotated[Session, Depends(get_async_db)], 
    params: orders_schema.OrdersParams = Depends(),
):
    list= await orders_crud.order_get_list(db, params.model_dump(exclude_unset=True, exclude_none=True))
    return{ 'list' : list }


# @router.get("/orders")
# async def orders_get_list(request: Request, db: Session = Depends(get_async_db), min_date=None, max_date=None, tid=None, oid=None, sid=None, status=None):
#     list= await orders_crud.order_get_list(db, min_date=min_date, max_date=max_date, tid=tid, oid=oid, sid=sid, status=status)
#     return{ 'list' : list }

    # total, list = await comm_crud.aync_get_list_all(Orders, db)
    # return {
    #     'total': total,
    #     'list': list
    # }

# Create
@router.post("/orders")
async def subscribe(
    item: orders_schema.OrdersCreate,
    db: Session = Depends(get_async_db),
):
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
    