import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional, Literal, List, Any




class Users(BaseModel):
    # id: str | None = None
    key: str | None = None
    name: str | None = None
    gender: str | None = None
    birthday: str | None = None
    phone: str | None = None
    email: str | None = None
    msg: str | None = None
    # create_date: str | None = None


class UserCreatePW(Users):
    password1: str
    password2: str