import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 

class Campaign(BaseModel):
    
    biz_title: str | None = None
    channel: str | None = None
    type: str | None = None
    category: str | None = None
    content: str | None = None 
    address: str | None = None
    phone: str | None = None
    msg: str | None = None 
    keyword: str | None = None 
    personnel: int | None = None
    available_dayname: str | None = None
    unvailable_dayname: str | None = None
    available_time: str | None = None

    run_start_date: datetime.datetime | None = None
    run_end_date: datetime.datetime | None = None
    apply_start_date: datetime.datetime | None = None
    apply_end_date: datetime.datetime | None = None
    create_date: datetime.datetime | None = None
    user_id: str | None = None

class CampaignRead(Campaign):
    id: int

class CampaignList(BaseModel):
    total: int = 0
    question_list: list[CampaignRead] = []


class CampaignCreate(Campaign):
    pass