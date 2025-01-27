import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional
from typing import List

class Subscription(BaseModel):
    endpoint: str
    keys: dict

class PushNotificationRequest(BaseModel):
    subscriptions: list[Subscription]
    message: str

class WebPush(BaseModel):
    key: str | None = None
    subscription: str | None = None
    msg: str | None = None



class WebPushDelete(BaseModel):
    id: int

class WebPushDeletes(BaseModel):
    ids: str | None = None
    
class WebPushUpdate(WebPush):
    id: int



class WebPushRead(WebPushUpdate):
    modify_date: datetime.datetime
    create_date: datetime.datetime
    

class WebPushCreate(WebPush):
    pass



class WebPushList(BaseModel):
    total: int = 0
    list: List[WebPushRead] = []

