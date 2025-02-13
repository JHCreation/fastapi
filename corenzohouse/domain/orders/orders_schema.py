import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional, Literal, List
from typing import List

from ..order_group.order_group_schema import OrderStatus


class Orders(BaseModel):
    key: str | None = None
    content: str | None = None
    order_id: str | None = None

class OrdersParams(BaseModel):
    min_date: str | None = None
    max_date: str | None = None
    tid: str | None = None
    oid: str | None = None
    sid: str | None = None
    status: OrderStatus | None = None

class OrdersDelete(BaseModel):
    id: str

class OrdersDeletes(BaseModel):
    ids: str | None = None
    
class OrdersUpdate(Orders):
    id: int



class OrdersRead(OrdersUpdate):
    modify_date: datetime.datetime
    create_date: datetime.datetime
    

class OrdersCreate(Orders):
    pass



class OrdersList(BaseModel):
    total: int = 0
    list: List[OrdersRead] = []

