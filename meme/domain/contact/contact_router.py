import os
from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Response, Request
from fastapi import Depends, Security
from fastapi.encoders import jsonable_encoder

from meme.database import get_db, get_async_db
from . import contact_schema
from meme.domain._comm import comm_crud, comm_schema
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from ...domain.user.user_auth import api_bearer_token
from ...model.contact import Contact

from ..mails.send_mail import send_naver_email, generate_email_html_1, send_gmail_email
from email.mime.text import MIMEText
from .contact_crud import contact_email
import copy
import asyncio
# import datetime

db= os.environ.get('DB_NAME')
router = APIRouter(
    prefix="/api/contact",
    tags=["meme contact"]
)
# print(oauth2_scheme.__dir__())

async def task(seconds):
    print(f'[작업시작] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    # 시작 메시지를 출력합니다. 작업이 몇 초 후에 끝날지 알려줍니다.
    print(f"이 작업은 {seconds} 초 뒤 종료됩니다.")
    
    # asyncio.sleep 함수를 사용하여 비동기적으로 지정된 시간 동안 대기합니다.
    # 'await'는 이 함수가 완료될 때까지 현재 코루틴의 실행을 일시 중지합니다.
    await asyncio.sleep(seconds)
    
    # 대기 시간이 끝나면, 작업 완료 메시지를 출력합니다.
    print(f"작업이 끝났습니다.")
    print(f'[작업종료] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    return { "status": f"{seconds} 성공!"}

async def prints (str):
    print(str)

@router.post("/test-send-email")
async def email_template(request: Request):
    
    # res= await asyncio.gather(
    #     task(1),
    #     task(2),
    #     task(3)
    # )
    # print(res)
    # return
    # await asyncio.gather(
    #     asyncio.sleep(2),
    #     prints('wait'),
    # )
    # return 'send!'

    email_context = {
        "name": 'test',
        "phone": '010-2826-8268',
        "email": 'corenzohouse@naver.com',
        "content": '????',
        "host": "https://www.memesition.com"
    }
    html= generate_email_html_1(
        request=request,
        template_name="contact.html",
        context=email_context
    ).body.decode()
    to= "corenzohouse@naver.com"
    msg= {
        "Subject": '테스트 메일입니다.',
        # "From": "corenzomarket@naver.com",
        "To": to,
    }
    content= MIMEText(html, 'html')
    res= await asyncio.gather(
        task(3),
        send_gmail_email(to_mail=to, mail_msg=msg, content=content),
        send_naver_email(to_mail=to, mail_msg=msg, content=content),
    )
    print(res)
    # return send_naver_email(to_mail=to, mail_msg=msg, content=content)

@router.get("/email-template")
def email_template(request: Request):
    # email_context = {
    #     "request": request,
    #     "event": "코렌초 파티",
    #     "price": 10000,
    #     "place": '건대 코렌초',
    #     "username": "홍길동",
    #     "verification_url": "https://example.com/verify?token=abc123",
    #     "items": ["상품1", "상품2", "상품3"],
    #     "test": test
    # }

    email_context = {
        "name": 'test',
        "phone": '010-2826-8268',
        "email": 'corenzohouse@naver.com',
        "content": '????',
        "host": "https://www.memesition.com"
    }
    return generate_email_html_1(
        request=request,
        template_name="contact.html",
        context=email_context
    )


 

@router.post("/create")
async def create(
    request: Request,
    item: contact_schema.ContactCreate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_async_db),
    # api_key: str = Security(api_bearer_token)
):  
    # category = category_crud.get_existing_category(db, category_create=item)
    # if category:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail="이미 존재하는 카테고리입니다.")
    update= {
        'create_date' : datetime.now(),
    }
    # print(type(item.model_dump()))
    # return
    email_context= item.model_dump()
    # await contact_email(request, context=email_context)
    # await send_naver_email(request, to_mail="corenzohouse@naver.com")
    # return
    print(f'[작업시작] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    res= await asyncio.gather(
        comm_crud.asyncCreate(Contact, db, item, res_id='id', update=update),
        contact_email(request, context=email_context),
    )

    # comm_crud.create(Contact, db, item, res_id='id', update=update)
    # await contact_email(request, context=email_context)
    
    print(f'[작업종료] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(res)
    return res[0]
    
    return 

@router.put("/update/{id}")
def update(
    # item,
    id: int,
    item: contact_schema.ContactCreate,
    # item: category_schema.CampaignCreate= Depends(),
    db: Session = Depends(get_db),
    api_key: str = Security(api_bearer_token)
):  
    # update= {
    #     'create_date' : datetime.now(),
    # }
    return comm_crud.update(Contact, db, item, filter_key='id', filter_value=id, res_id='key')

@router.get("/list", response_model=contact_schema.ContactList)
def list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, list = comm_crud.get_list(
        Contact, db, skip=page*size, limit=size)
    
    # time.sleep(5)
    # print('lisssssssss')
    return {
        'total': total,
        'list': list
    }

@router.get("/{id}",)
def list( id: int, db: Session = Depends(get_db) ):
    datas = comm_crud.get_item(
        Contact, db, key='id', value=id)
    data= datas.first()
    # time.sleep(5)
    return data
    # print('lisssssssss')
    return {
        'total': total,
        'list': list
    }


@router.post("/list", 
            #  response_model=category_schema.CategoryList
            )
def list(item:comm_schema.CommFilterList,
                  db: Session = Depends(get_db),
                  ):
    page, size, filter= item
    page= page[1]
    size= size[1]
    filter= filter[1]
    filters= eval(filter)
    # print(filter)

    total, list = comm_crud.get_list(
        Contact, db, skip=page*size, limit=size, filter=filters)
    
    return {
        'total': total,
        'list': list
    }