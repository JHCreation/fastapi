import os
from sqlalchemy.orm import Session
from ...domain.webpush.webpush_schema import WebPushCreate, WebPushUpdate
from ...model.webpush import WebPush
from datetime import datetime
from sqlalchemy import select, func, or_
from starlette import status
from fastapi import APIRouter, HTTPException, Response, Request
import json
from ...domain.webpush import webpush_schema
from ...config import ROOT_DIR
from dotenv import load_dotenv
from pywebpush import webpush, WebPushException
import re
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)

VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY')
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY')
# VAPID_CLAIMS = {
#     "sub": f"mailto:{os.environ.get('VAPID_CLAIMS')}"
# }
VAPID_CLAIMS_EMAIL = os.environ.get('VAPID_CLAIMS')

def get_push_service(endpoint):
    if re.match(r"^https:\/\/fcm\.googleapis\.com\/fcm\/send\/.*", endpoint):
        return "https://fcm.googleapis.com"
    elif re.match(r"^https:\/\/web\.push\.apple\.com\/.*", endpoint):
        return "https://web.push.apple.com"
    else:
        return ""

def delete_subcription():
    return

async def send_webpush(subscription: webpush_schema.Subscription, message: str):
    # print(({
    #             "endpoint": subscription['endpoint'],
    #             "keys": subscription['keys'],
    #         }))
    try:
        push_service= get_push_service(subscription['endpoint'])
        # print(push_service)
        # return
        vapid_claims= { 
            "sub": f"mailto:{VAPID_CLAIMS_EMAIL}",
            "aud": push_service,
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