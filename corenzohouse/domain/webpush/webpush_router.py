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
from ...domain.webpush import webpush_crud, webpush_schema
# from webpush_schema import Subscription
from pywebpush import webpush, WebPushException
from pydantic import ValidationError
import json

# from corenzohouse.route import router, router2
from corenzohouse.database import get_db, get_async_db
from ...domain._comm import comm_crud

# from _utils.crud import comm_crud

# from ...config import ROOT_DIR
# from dotenv import load_dotenv
from ...model.webpush import WebPush, WebPushLog
# load_dotenv()
# load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

router = APIRouter()

VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY')
# VAPID_CLAIMS = {
#     "sub": f"mailto:{os.environ.get('VAPID_CLAIMS')}"
# }
VAPID_CLAIMS_EMAIL = os.environ.get('VAPID_CLAIMS')

@router.get("/subscribe", 
            #  status_code=status.HTTP_204_NO_CONTENT
             )
async def webpush_get_subscribe(request: Request, db: Session = Depends(get_async_db)):
    total, list = await comm_crud.aync_get_list_all(WebPush, db)
    return {
        'total': total,
        'list': list
    }
    return {'webpush test': str(request.base_url)}

# Create
@router.post("/subscribe")
async def subscribe(
    item: webpush_schema.WebPushCreate,
    db: Session = Depends(get_async_db),
):
    # 구독 정보를 데이터베이스에 저장하는 로직을 여기에 구현
    update= {
        'modify_date' : datetime.now(),
        'create_date' : datetime.now(),
    }
    
    # return
    return await comm_crud.asyncCreate(WebPush, db, item, res_id='endpoint', update=update)
    # return {"message": "Subscription successful"}

@router.delete("/subscribe")
async def subscribe(
    item: webpush_schema.WebPushDelete,
    db: Session = Depends(get_async_db),
):
    print(item)
    # return 'delete test'
    return await comm_crud.asyncDelete(WebPush, db, filter_key='endpoint', filter_value=item.endpoint, res_id='id')
    

@router.post("/push-bulk")
# async def send_push_bulk(request: webpush_schema.PushNotificationRequest, db: Session = Depends(get_async_db)):
async def push_notification(
    request: Request,
    db: Session = Depends(get_async_db),
    data= Body(...),
    # item= Body(...),
    # item: category_schema.CampaignCreate= Depends(),
    # db: Session = Depends(get_async_db),
):
    return await webpush_crud.push_notification_bulk(db, data)

@router.post("/push")
async def push_notification(
    request: Request,
    # subscription: webpush_schema.Subscription,
    data= Body(...),
    item= Body(...),
    # item: category_schema.CampaignCreate= Depends(),
    # db: Session = Depends(get_async_db),
):
    # 실제 구현에서는 데이터베이스에서 구독 정보를 가져와야 함
    # subscription_info = {
    #     "endpoint": "https://fcm.googleapis.com/fcm/send/...",
    #     "keys": {
    #         "p256dh": "user_public_key",
    #         "auth": "user_auth_secret"
    #     }
    # }
    
    print(data)
    return
    try:
        webpush(
            subscription_info=subscription.model_dump(),
            data=json.dumps(data),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        return {"message": "Push notification sent"}
    except WebPushException as e:
        raise HTTPException(status_code=500, detail=str(e))