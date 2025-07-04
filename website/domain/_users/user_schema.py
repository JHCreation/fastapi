import datetime
from pydantic import BaseModel, field_validator, EmailStr, Field, model_validator
from pydantic_core.core_schema import FieldValidationInfo
from typing import List, Optional

userid_fields= Field(None, min_length=3, max_length=50)
class UsersBase(BaseModel):
    userid: str | None = None
    password: str | None = None
    email: str | None = None
    phone: str | None = None
    username: str | None = None
    usertype: str | None = None
    permission: str | None = None
    nickname: str | None = None
    orgname: str | None = None
    domain: str | None = None

class UsersUpdate(UsersBase):
    id: int

class UsersRead(UsersUpdate):
    modify_date: datetime.datetime
    create_date: datetime.datetime

class UsersCreate(UsersBase):
    userid: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)
    password_confirm: str = Field(..., min_length=4)

    @field_validator('userid', 'password', 'password_confirm')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return self

class UsersUpdate(UsersBase):
    userid: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=4)
    password_confirm: Optional[str] = Field(None, min_length=4)

    @field_validator('userid', 'password', 'password_confirm')
    def not_empty_if_present(cls, v):
        if v is not None and not v.strip():
            raise ValueError("공백만 있는 값은 허용되지 않습니다.")
        return v

    @model_validator(mode='after')
    def check_passwords_match_if_present(self):
        if self.password and self.password_confirm:
            if self.password != self.password_confirm:
                raise ValueError("비밀번호가 일치하지 않습니다.")
        return self

class UsersDeletes(BaseModel):
    ids: List[str|int] | None = None









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