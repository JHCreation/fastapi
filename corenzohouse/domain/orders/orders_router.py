import os
from datetime import timedelta, datetime
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi import FastAPI, Body
import asyncio

from ...database import get_db, get_async_db
from ...domain.orders import orders_crud, orders_schema
# from orders_schema import Subscription
from pydantic import ValidationError
import json

# from corenzohouse.route import router, router2
from corenzohouse.database import get_db, get_async_db
from ...domain._comm import comm_crud

# from _utils.crud import comm_crud

from ...config import ROOT_DIR
from dotenv import load_dotenv
from ...model.orders import Orders, OrderGroup
from ...domain.webpush import webpush_crud


load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

# from orders_crud import order_get_list
router = APIRouter()

@router.get("/orders")
async def orders_get_list(
    request: Request, 
    db: Annotated[Session, Depends(get_async_db)], 
    params: orders_schema.OrdersParams = Depends(),
):
    list= await orders_crud.order_get_list(db, params.model_dump(exclude_unset=True, exclude_none=True))
    return{ 'list' : list }

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

@router.delete("/orders-item")
async def subscribe(
    item: orders_schema.OrdersItemDelete,
    db: Session = Depends(get_async_db),
):
    print(item)
    # return
    return await comm_crud.asyncDelete(Orders, db, filter_key='key', filter_value=item.key, res_id='key')

@router.delete("/orders")
async def subscribe(
    item: orders_schema.OrdersDelete,
    db: Session = Depends(get_async_db),
):
    print(item)
    # return
    return await comm_crud.asyncDelete(Orders, db, filter_key='order_id', filter_value=item.order_id, res_id='order_id')
  

@router.post("/orders-group")
async def subscribe(
    background_tasks: BackgroundTasks,
    item: orders_schema.Orders_Group= Body(...),
    # item: orders_schema.Orders_Group,
    # params: orders_schema.Orders_Group,
    db: AsyncSession = Depends(get_async_db),
):
    params= item.model_dump(exclude_none=True)
    update= {
        'modify_date' : datetime.now(),
        'create_date' : datetime.now(),
    }
    
    # if params['push'] == True:
    pushData= json.loads(params['orders']['content'])
    pushData['id']= params['orders']['key']
    pushData['title']= params['title']
    pushData['push']= params['push']
    # print(pushData)
    # push_result= await webpush_crud.push_notification_bulk(db, pushData)
    # asyncio.create_task(webpush_crud.push_notification_bulk(db, pushData))
    background_tasks.add_task(webpush_crud.push_notification_bulk, db, pushData)


    group_result= 'pass'
    if 'group' in params and params.get('group') is not None:
        group_result= await comm_crud.asyncCreate(OrderGroup, db, params['group'], res_id='id', update=update)

    
    
    orders_result= await comm_crud.asyncCreate(Orders, db, params['orders'], res_id='id', update=update)
        
    return {
        'group': group_result,
        'orders': orders_result
    }
    