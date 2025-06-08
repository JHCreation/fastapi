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
from ...domain.reviewers import reviewers_crud, reviewers_schema
# from reviewers_schema import Subscription
from pydantic import ValidationError
import json

from corenzohouse.route import router, router2
from corenzohouse.database import get_db, get_async_db
from ...domain._comm import comm_crud

# from _utils.crud import comm_crud

from ...config import ROOT_DIR
from dotenv import load_dotenv
from ...model.reviewers import Reviewers
from ...domain.webpush import webpush_crud
import httpx
import time
import logging


load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# from reviewers_crud import order_get_list

@router.get("/reviewers")
async def orders_get_list(
    request: Request, 
    db: Annotated[Session, Depends(get_async_db)], 
    params: reviewers_schema.Reviewers = Depends(),
):
    list= await reviewers_crud.reviewers_get_list(db, params.model_dump(exclude_unset=True, exclude_none=True))
    return{ 'list' : list }


@router.post("/reviewers")
async def subscribe(
    item: reviewers_schema.Reviewers,
    db: Session = Depends(get_async_db),
):
    print(item)
    # return
    update= {
        # 'modify_date' : datetime.now(),
        'create_date' : datetime.now(),
    }
    return await comm_crud.asyncCreate(Reviewers, db, item, res_id='id', update=update)

@router.post("/reviewers-confirm")
async def confirmed(
    item= Body(...),
):
    logger.debug(item, type(item))   # 기본적으로 출력되지 않음 (DEBUG는 INFO보다 낮음)

    accessKey='DfniYnHiwvbNVF2dEmjo'
    secretKey='pGHJknpOG3PrqfWajFDojC8RVJII2kVarhiHseE9'

    # {
    #     "type": "SMS",
    #     "countryCode": "82",
    #     "from": "01028268268",
    #     "subject": "string",
    #     "contentType": "COMM",
    #     "content": "test.",
    #     "messages": [
    #         {
    #         "subject": "subject?",
    #         "content": "test...!!!!!",
    #         "to": "01028268268"
    #         }
    #     ]
    # }

    result = []
    for param in item:

        timestamp = int(time.time() * 1000)
        timestamp = str(timestamp)
        signature= reviewers_crud.make_signature(accessKey=accessKey, secretKey=secretKey, timestamp=timestamp)
        url = "https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:257063279563:jhc-message/messages"
        
        headers = {
            'Content-Type': 'application/json',
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": accessKey,
            "x-ncp-apigw-signature-v2": signature
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=param, headers=headers)
            result.append({"status_code": response.status_code, "response": response.json()})
        
    return result 