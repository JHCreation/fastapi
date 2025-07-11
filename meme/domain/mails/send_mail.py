import os
import smtplib
import re  # Regular Expression을 활용하기 위한 모듈
from email.mime.multipart import MIMEMultipart  # 메일의 Data 영역의 메시지를 만드는 모듈
from email.mime.text import MIMEText  # 메일의 본문 내용을 만드는 모듈
from email.mime.image import MIMEImage  # 메일의 이미지 파일을 base64 형식으로 변환하기 위한 모듈
from ...config import ROOT_DIR
from dotenv import load_dotenv
import asyncio

# load_dotenv()
load_dotenv(dotenv_path=f'{ROOT_DIR}/.env', override=True)
SMTP_NAVER_EMAIL_ACCOUNT= os.environ.get('SMTP_NAVER_EMAIL_ACCOUNT')
SMTP_NAVER_EMAIL_PASSWORD= os.environ.get('SMTP_NAVER_EMAIL_PASSWORD')
SMTP_GOOGLE_EMAIL_ACCOUNT= os.environ.get('SMTP_GOOGLE_EMAIL_ACCOUNT')
SMTP_GOOGLE_EMAIL_PASSWORD= os.environ.get('SMTP_GOOGLE_EMAIL_PASSWORD')
# print('email',SMTP_GOOGLE_EMAIL_ACCOUNT, SMTP_GOOGLE_EMAIL_PASSWORD)

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
print('BASE_DIR', BASE_DIR)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
# app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def test(str):
    return f"Hello, {str}!"

def generate_email_html_1(request: Request, template_name: str, context: dict) -> str:
    context["request"] = request  # Jinja2Templates requires this
    return templates.TemplateResponse(
        template_name,
        context,
    )

async def generate_email_html(request: Request, template_name: str, context: dict) -> str:
    """이메일 템플릿을 렌더링하는 함수"""
    context["request"] = request  # Jinja2Templates requires this
    return templates.TemplateResponse(
        template_name,
        context,
    ).body.decode()


def sendEmails(smtp, addr, account, to_mail, msg):
    reg = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"  # 유효성 검사를 위한 정규표현식
    
    if re.match(reg, addr):
        smtp.sendmail(account, to_mail, msg.as_string())
        print("정상적으로 메일이 발송되었습니다.")
    else:
        print("받으실 메일 주소를 정확히 입력하십시오.")



msgs= {
    "Subject": '',
    "To": '',
}


async def send_gmail_email(to_mail='', mail_msg=msgs, content=None):
    print('gmail')
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    account = SMTP_GOOGLE_EMAIL_ACCOUNT
    password = SMTP_GOOGLE_EMAIL_PASSWORD
    smtp.ehlo()
    # await asyncio.sleep(0)
    send_email(smtp=smtp, account=account, password=password, to_mail=to_mail, mail_msg=mail_msg, content=content)

async def send_naver_email(to_mail='', mail_msg=msgs, content=None):
    print('naver')
    smtp = smtplib.SMTP('smtp.naver.com', 587)
    account = SMTP_NAVER_EMAIL_ACCOUNT
    password = SMTP_NAVER_EMAIL_PASSWORD
    smtp.ehlo()
    smtp.starttls()
    # await asyncio.sleep(0)
    send_email(smtp=smtp, account=account, password=password, to_mail=to_mail, mail_msg=mail_msg, content=content)

def send_email(smtp=None, account='', password='', to_mail='', mail_msg=msgs, content=None):

    smtp.login(account, password)
    # to_mail = "corenzohouse@naver.com"
    msg = MIMEMultipart()
    msg["From"] = account
    # msg["From"] = "corenzomarket@naver.com"
    for key, val in mail_msg.items():
        msg[key]= val
    
    # print(msg["From"])
    # return
#   msg["Subject"] = f"첨부 파일 확인 바랍니다"  # 메일 제목
#   msg["From"] = account
#   msg["To"] = to_mail

  # 메일 본문 내용
#   content = "안녕하세요. naver\n\n\
#   데이터를 전달드립니다.\n\n\
#   감사합니다\n\n\
#   "
#   content_part = MIMEText(content, "plain")


#   email_context = {
#       "username": "홍길동",
#       "verification_url": "https://example.com/verify?token=abc123",
#       "items": ["상품1", "상품2", "상품3"],
#   }
  
  # HTML 이메일 생성
#   html_content = await generate_email_html(
#       request=request,
#       template_name="email_template.html",
#       context=email_context
#   )
#   print(html_content)
#   content_html = MIMEText(html_content, 'html')
    msg.attach(content)
    print('이메일 전송 시작')
    # await asyncio.sleep(0)

    smtp.sendmail(account, to_mail, msg.as_string())
    smtp.quit()
    print('이메일 전송 완료')
    return 'email success'
  
    # 이미지 파일 추가
    image_name = "test.png"
    with open(image_name, 'rb') as file:
        img = MIMEImage(file.read())
        img.add_header('Content-Disposition', 'attachment', filename=image_name)
        msg.attach(img)
    
    # 받는 메일 유효성 검사 거친 후 메일 전송
    sendEmail(to_mail)
    
    # smtp 서버 연결 해제
    smtp.quit()
    return