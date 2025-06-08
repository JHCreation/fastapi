import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional, Literal, List, Any

from ..order_group.order_group_schema import OrderStatus, OrderGroup



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

class Orders_Group(Orders):
    push: bool
    orders: Orders | None = None
    group: OrderGroup | None = None
    title: str

class OrdersItemDelete(BaseModel):
    key: str

class OrdersDelete(BaseModel):
    order_id: str
    
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

