import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional, Literal, List, Any




class Reviewers(BaseModel):
    # id: str | None = None
    key: str | None = None
    name: str | None = None
    channel: str | None = None
    gender: str | None = None
    birthday: str | None = None
    phone: str | None = None
    email: str | None = None
    link: str | None = None
    wish_drink: str | None = None
    msg: str | None = None
    # create_date: str | None = None