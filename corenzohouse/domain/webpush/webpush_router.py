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

from corenzohouse.route import router, router2
from corenzohouse.database import get_db, get_async_db
from ...domain._comm import comm_crud

# from _utils.crud import comm_crud

from ...config import ROOT_DIR
from dotenv import load_dotenv
from ...model.webpush import WebPush
import re
# load_dotenv()
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

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
    return await comm_crud.asyncCreate(WebPush, db, item, res_id='id', update=update)
    # return {"message": "Subscription successful"}
def get_push_service(endpoint):
    """
    푸시 서비스 유형(Firebase 또는 APNs)을 반환합니다.

    Args:
        endpoint (str): 구독 정보의 endpoint URL

    Returns:
        str: 'FCM' 또는 'APNs' 또는 'Unknown'
    """
    if re.match(r"^https:\/\/fcm\.googleapis\.com\/fcm\/send\/.*", endpoint):
        return "https://fcm.googleapis.com"
    elif re.match(r"^https:\/\/web\.push\.apple\.com\/.*", endpoint):
        return "https://web.push.apple.com"
    else:
        return ""
async def send_webpush(subscription: webpush_schema.Subscription, message: str):
    print(({
                "endpoint": subscription['endpoint'],
                "keys": subscription['keys'],
            }))
    try:
        push_service= get_push_service(subscription['endpoint'])
        # print(push_service)
        # return
        vapid_claims= { 
            "sub": f"mailto:{VAPID_CLAIMS_EMAIL}",
            "aud": push_service
        }
        webpush(
            subscription_info={
                "endpoint": subscription['endpoint'],
                "keys": subscription['keys'],
            },
            data=message,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=vapid_claims,
            
        )
    except WebPushException as ex:
        # 실패한 경우 로그를 남기거나 에러 처리
        return {"endpoint": subscription['endpoint'], "status": "failed", "error": str(ex)}
    return {"endpoint": subscription['endpoint'], "status": "success"}

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
    # 모든 구독자에게 비동기로 푸시 알림 보내기
    total, list = await comm_crud.aync_get_list_all(WebPush, db)
    # print(total, list)
    subscriptions = [json.loads(item.subscription) for item in list if item.subscription]
    # print( subscriptions, type(subscriptions) )
    # for item in list:
    #     print(type(json.loads(item.subscription)))
    # return {
    #     'total': total,
    #     'list': list
    # }
    
    tasks = [
        send_webpush(subscription, json.dumps(data))
        # for subscription in request.subscriptions
        for subscription in subscriptions
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 결과 반환
    response = []
    for subscription, result in zip(subscriptions, results):
        # print('subscription', subscription)
        if isinstance(result, Exception):
            response.append({
                "endpoint": subscription['endpoint'],
                "status": "failed",
                "error": str(result)
            })
        else:
            response.append(result)
    return {"results": response}

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