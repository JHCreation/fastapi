import os
from fastapi import APIRouter, Request
from ...mail.send_mail import send_naver_email
from email.mime.text import MIMEText
import asyncio
from ....config import logger, ROOT_DIR
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ....lib.format import format_phone_number, nl2br
from dotenv import load_dotenv

router = APIRouter(
    prefix="/contact",
)

load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)
EMAIL_ACCOUNT_MAPOCLEAN= os.environ.get('EMAIL_ACCOUNT_MAPOCLEAN')
EMAIL_PASSWORD_MAPOCLEAN= os.environ.get('EMAIL_PASSWORD_MAPOCLEAN')
BASE_DIR= Path(__file__).resolve().parent.parent.parent / 'mail' / 'templates'
templates = Jinja2Templates( directory=str(BASE_DIR) )
# templates.env.filters["nl2br"] = nl2br

@router.post("/send-email")
async def email_template(request: Request):
    data = await request.json()
    email_context= {
        "request": request,
        "host": "https://www.mapoclean.com",
        "data": {
            "문의타입": ", ".join(data['category']),
            "업체/회사명": data['org_name'],
            "이름": data['name'],
            "이메일": data['email'],
            "연락처": format_phone_number(data['phone']),
            "문의내용": nl2br(data['msg']),
        }
    }
    # logger.debug(email_context)

    html= templates.TemplateResponse(
        "contact.html",
        email_context,
    ).body.decode()
    to= EMAIL_ACCOUNT_MAPOCLEAN
    msg= {
        "Subject": '문의메일입니다.',
        "To": to,
    }
    content= MIMEText(html, 'html')
    res= await asyncio.gather(
        send_naver_email(to_mail=to, mail_msg=msg, content=content, account=EMAIL_ACCOUNT_MAPOCLEAN, password=EMAIL_PASSWORD_MAPOCLEAN),
    )

    return res


@router.get("/email-template")
def email_template(request: Request):

    email_context = {
        "request": request,
        "host": "http://mapoclean.com",
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