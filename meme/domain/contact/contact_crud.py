import os
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException, Response, Request
from ..mails.send_mail import send_naver_email, generate_email_html_1, send_gmail_email
from ...config import ROOT_DIR
from dotenv import load_dotenv
# load_dotenv()
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)
STATIC_HOST= os.environ.get('STATIC_HOST')

async def contact_email(request: Request, context: None, ):
    print('이메일 보내기 시작')

    email_context= context
    email_context['host']= STATIC_HOST
    
    html= generate_email_html_1(
        request=request,
        template_name="contact.html",
        context=email_context
    ).body.decode()

    # to= email_context['email']
    to= 'corenzohouse@naver.com'
    msg= {
        "Subject": f"{email_context['name']}님의 문의 메일입니다.",
        # "From": "corenzomarket@naver.com",
        "To": to,
    }
    content= MIMEText(html, 'html')
    return await send_gmail_email(to_mail=to, mail_msg=msg, content=content)
    # return send_naver_email(to_mail=to, mail_msg=msg, content=content)