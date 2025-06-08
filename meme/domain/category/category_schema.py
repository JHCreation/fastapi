import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import List, Any

# class Category(BaseModel):
#     key: str | None = None
#     name: str | None = None
#     value: List[Any] | None = None
#     status: str | None = None
#     doc_01: List[str] | None = None
#     doc_02: str | None = None
#     # create_date: datetime.datetime
#     user_id: int | None = None

class Category(BaseModel):
    key: str | None = None
    name: str | None = None
    value: str | None = None
    status: str | None = None
    doc_01: str | None = None
    doc_02: str | None = None
    # create_date: datetime.datetime
    user_id: int | None = None


class CategoryDelete(BaseModel):
    id: int

class CategoryDeletes(BaseModel):
    ids: str | None = None



class CategoryRead(Category):
    id: int
    modify_date: datetime.datetime
    create_date: datetime.datetime
    

class CategoryCreate(Category):
    key: str | None = None
    name: str | None = None
    value: List[Any] | None = None
    status: str | None = None
    doc_01: List[str] | None = None
    doc_02: List[str] | None = None
    # create_date: datetime.datetime
    user_id: int | None = None

class CategoryUpdate(CategoryCreate):
    id: str


class CategoryList(BaseModel):
    total: int = 0
    list: List[CategoryRead] = []