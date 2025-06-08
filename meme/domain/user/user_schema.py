import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional

class User(BaseModel):
    userid: str

class UserUpdate(BaseModel):
    # password1: str | None = None
    # password2: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    username: str | None = None
    nickname: str | None = None
    usertype: str | None = None
    # modify_date: datetime.datetime | None = None
    # create_date: datetime.datetime | None = None
    sns_type: str | None = None
    sns_id: str | None = None
    sns_connect_date: str | None = None
    sns_name: str | None = None
    sns_gender: str | None = None
    sns_age: str | None = None
    sns_birthyear: str | None = None
    sns_birthday: str | None = None
    permission: str | None = None

class UserCreate(User):
    # password1: str
    # password2: str
    phone: str
    email: EmailStr
    username: str
    nickname: str
    usertype: str
    # modify_date: datetime.datetime
    # create_date: datetime.datetime
    sns_type: str
    sns_id: str
    sns_connect_date: str
    sns_name: str
    sns_gender: str
    sns_age: str
    sns_birthyear: str
    sns_birthday: str
    permission: str
    

    @field_validator('userid', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    # @field_validator('userid', 'password1', 'password2', 'email')
    # def not_empty(cls, v):
    #     if not v or not v.strip():
    #         raise ValueError('빈 값은 허용되지 않습니다.')
    #     return v

    # @field_validator('password2')
    # def passwords_match(cls, v, info: FieldValidationInfo):
    #     if 'password1' in info.data and v != info.data['password1']:
    #         raise ValueError('비밀번호가 일치하지 않습니다')
    #     return v

class RefreshToken(BaseModel):
    refresh_token: str

class Token(BaseModel):
    access_token: str
    token_type: str
    userid: str
    refresh_token: Optional[str] = None 


class JWT(BaseModel):
    exp: int
    sub: str


class UserCreatePW(UserCreate):
    password1: str
    password2: str

    # @field_validator('userid', 'email')
    # def not_empty(cls, v):
    #     if not v or not v.strip():
    #         raise ValueError('빈 값은 허용되지 않습니다.')
    #     return v

    @field_validator('userid', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v