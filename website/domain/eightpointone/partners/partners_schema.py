import datetime
from pydantic import BaseModel, ConfigDict
from typing import List

class PartnersBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    key: str | None = None
    title: str | None = None
    subject: str | None = None
    contents: str | None = None
    images: list | None = None
    public: str | None = None
    category: str | None = None
    link: str | None = None


class PartnersDeletes(BaseModel):
    ids: List[str|int] | None = None
    
class PartnersUpdate(PartnersBase):
    id: int

class PartnersRead(PartnersUpdate):
    # modify_date: datetime.datetime
    create_date: datetime.datetime
    

class PartnersCreate(PartnersBase):
    pass



class PartnersList(BaseModel):
    total: int = 0
    list: List[PartnersRead] = []