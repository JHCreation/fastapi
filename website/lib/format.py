import re

def format_phone_number(phone: str) -> str:
    # 휴대폰 번호 (11자리 또는 10자리) 처리
    return re.sub(r"^(\d{3})(\d{3,4})(\d{4})$", r"\1-\2-\3", phone)

def nl2br(value: str) -> str:
    return re.sub(r'\r\n|\r|\n', '<br>', value)