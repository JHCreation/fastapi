import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional, Literal, List
from typing import List
from enum import Enum
from fastapi import FastAPI, Depends, Query

class OrderStatus(str, Enum):
    USE = "use"
    PAID = "paid"

class OrderGroupParams(BaseModel):
    tid: str | None = None
    sale_date: str | None = None
    status: OrderStatus | None = None

class OrderGroupsParams(BaseModel):
    # tid: list = Query(...)
    status: OrderStatus = None
    tid: List[str] = Query(None)

class OrderGroup(BaseModel):
    content: str | None = None
    order_id: str | None = None
    store_id: str | None = None
    table_id: str | None = None
    status: OrderStatus = None
    # store_id: str | None = None
    # table_id: str | None = None
    # status: Optional[Literal["use", "paid"]] = None

class OrderGroupDelete(BaseModel):
    id: str

class OrderGroupDeletes(BaseModel):
    ids: str | None = None
    
class OrderGroupUpdate(OrderGroup):
    id: int



class OrderGroupRead(OrderGroupUpdate):
    modify_date: datetime.datetime
    create_date: datetime.datetime
    

class OrderGroupCreate(BaseModel):
    order_id: str 
    store_id: str 
    table_id: str 
    sale_date: str
    status: OrderStatus



class OrderGroupList(BaseModel):
    total: int = 0
    list: List[OrderGroupRead] = []

