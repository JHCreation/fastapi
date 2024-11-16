import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class User(BaseModel):
    userid: str

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

class Token(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str
    userid: str




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