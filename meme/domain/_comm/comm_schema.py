import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Any, List, Sequence, TypeVar


class CommList(BaseModel):
    total: int = 0
    list: Any


class CommFilterList(BaseModel):
    page: int = 0
    size: int = 10
    filter: str = None