import os
from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, Query
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from fastapi import FastAPI, Body
import asyncio

from ...database import get_db, get_async_db
from ...domain.order_group import order_group_crud, order_group_schema
from ...domain.orders import orders_crud, orders_schema
# from orders_schema import Subscription
from pydantic import ValidationError
import json

from corenzohouse.route import router, router2
from corenzohouse.database import get_db, get_async_db
from ...domain._comm import comm_crud

# from _utils.crud import comm_crud
from typing import List
from ...config import ROOT_DIR
from dotenv import load_dotenv
from ...model.orders import OrderGroup
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

import logging

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
# from orders_crud import order_get_list
# def common_parameters(q: str | None = None, skip: int = 0, limit: int = 10):
#     return {"q": q, "skip": skip, "limit": limit}
def get_tids(params: order_group_schema.OrderGroupsParams = Depends()):
    return params


@router.get("/order-groups")
async def order_group_get_list(
    db: Annotated[Session, Depends(get_async_db)], 
    params: order_group_schema.OrderGroupParams = Depends(),
):

    groups= await order_group_crud.order_group_get_list(db, params.model_dump(exclude_unset=True, exclude_none=True))
    if not groups:
        raise HTTPException(status_code=404, detail="Order Group not found")
    groupIds= [order.order_id for order in groups]
    data= await orders_crud.order_get_list(db, { 'oid': groupIds })

    return {
        'group': groups,
        'list': data
    }
    

@router.get("/order-group")
# async def order_group_get_list(request: Request, db: Session = Depends(get_async_db), min_date=None, max_date=None, tid=None, oid=None, sid=None, status=None):
async def order_group_get_list(
    request: Request, 
    db: Annotated[Session, Depends(get_async_db)], 
    # item: dict = Depends(common_parameters),
    params: order_group_schema.OrderGroupParams = Depends(),
):
    logger.info('get order')
    # params = dict(request.query_params)
    order= await order_group_crud.order_group_get_item(db, params.model_dump(exclude_unset=True, exclude_none=True))
    if not order:
        raise HTTPException(status_code=404, detail="Order Group not found")
    
    list= await orders_crud.order_get_list(db, { 'oid': order.order_id })

    return {
        'id': order.order_id, 
        'list': list
    }
    

# Create
@router.post("/order-group")
async def createOrderGroup(
    item: order_group_schema.OrderGroupCreate,
    db: Session = Depends(get_async_db),
):
    update= {
        'modify_date' : datetime.now(),
        'create_date' : datetime.now(),
    }
    return await comm_crud.asyncCreate(OrderGroup, db, item, res_id='id', update=update)


@router.put("/order-group/{order_id}")
async def updateOrderGroup(
    order_id: str,
    params: order_group_schema.OrderGroup = Body(...),
    db: Session = Depends(get_async_db),
):
    update= {
        'modify_date' : datetime.now(),
    }
    return await comm_crud.asyncUpdate(OrderGroup, db, params, filter_key='order_id', filter_value=order_id, res_id='order_id', update=update)

# @router.delete("/orders")
# async def subscribe(
#     item: orders_schema.OrdersDelete,
#     db: Session = Depends(get_async_db),
# ):
#     print(item)
#     return await comm_crud.asyncDelete(Orders, db, filter_key='id', filter_value=item.endpoint, res_id='id')
    