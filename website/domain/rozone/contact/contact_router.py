import os
from fastapi import APIRouter, Request
from ...mail.send_mail import send_naver_email, send_naverWorks_email
from email.mime.text import MIMEText
import asyncio
from ....config import logger, ROOT_DIR
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ....lib.format import format_phone_number, nl2br
from ..web_router import DOMAIN_WWW, EMAIL_ACCOUNT, EMAIL_PASSWORD, EMAIL_TO
router = APIRouter(
    prefix="/contact",
)

BASE_DIR= Path(__file__).resolve().parent.parent.parent / 'mail' / 'templates'
templates = Jinja2Templates( directory=str(BASE_DIR) )
# templates.env.filters["nl2br"] = nl2br

@router.post("/send-email")
async def email_template(request: Request):
    data = await request.json()
    email_context= {
        "request": request,
        "host": DOMAIN_WWW,
        "data": {
            "문의타입": ", ".join(data['category']),
            "업체/회사명": data['org_name'],
            "이름": data['name'],
            "이메일": data['email'],
            "연락처": format_phone_number(data['phone']),
            "문의내용": nl2br(data['msg']),
        }
    }

    html= templates.TemplateResponse(
        "contact.html",
        email_context,
    ).body.decode()
    to= EMAIL_TO
    msg= {
        "Subject": '문의메일입니다.',
        "To": to,
    }
    content= MIMEText(html, 'html')
    res= await asyncio.gather(
        send_naver_email(to_mail=to, mail_msg=msg, content=content, account=EMAIL_ACCOUNT, password=EMAIL_PASSWORD),
    )

    return res


@router.get("/email-template")
def email_template(request: Request):

    email_context = {
        "request": request,
        "host": DOMAIN_WWW,
        "data": {
            # "name": 'test',
            # "phone": '010-2826-8268',
            # "email": 'corenzohouse@naver.com',
            # "content": '????'
            "분류": ['test', 'abcd'],
            "업체명": "jhc",
            "이름": "유주형",
            "이메일": "myz@naver.com",
            "연락처": format_phone_number("01028268268"),
            "문의내용": nl2br('test...\n문의 내용입니다.'),
        }
    }
    return templates.TemplateResponse(
        "contact.html",
        email_context,
    )