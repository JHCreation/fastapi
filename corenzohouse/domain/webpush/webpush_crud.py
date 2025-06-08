import os
from datetime import datetime
import json
from ...config import ROOT_DIR
from dotenv import load_dotenv
from pywebpush import webpush, WebPushException
import re
import asyncio
from ...domain.webpush import webpush_crud, webpush_schema
from ...domain._comm import comm_crud
from ...model.webpush import WebPush, WebPushLog

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...database import async_session_factory

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


async def webpush_get_list( model, db:AsyncSession, params: dict ):
    # async with async_session_factory() as db:
        query = select(model)
        if params.get('status') is not None:
            query = query.where(model.status == params['status'])
        
        query= query.order_by(model.id.desc())
        result= await db.execute(query)
        data = result.scalars().all()
        return data

async def push_notification_bulk( db, data ):
    # print('푸시진입!!!!!!!!!!')
    async with async_session_factory() as db:
        # 모든 구독자에게 비동기로 푸시 알림 보내기
        list = await webpush_get_list(WebPush, db, {'status': 'use'})
        # return
        # total, list = await comm_crud.aync_get_list_all(WebPush, db)
        # print(total, list)
        subscriptions = [json.loads(item.subscription) for item in list if item.subscription]
        # print( subscriptions, type(subscriptions) )
        # for item in list:
        #     print(type(json.loads(item.subscription)))
        # return {
        #     'total': total,
        #     'list': list
        # }
        payload={
            "notification": data,
            "data": {
                "sender": "홍길동"  # 발신자 이름을 custom_data로 포함
            }
        }

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

        update= {
            'create_date' : datetime.now(),
        }
        log_res= await comm_crud.asyncCreate(WebPushLog, db, { 'log': str(response) }, res_id="id", update=update)
        
    return {"results": response}