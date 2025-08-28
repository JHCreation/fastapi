import datetime
from pydantic import BaseModel, ConfigDict
from typing import List

class NewsBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    key: str | None = None
    title: str | None = None
    subject: str | None = None
    contents: str | None = None
    images: list | None = None
    public: str | None = None


class NewsDeletes(BaseModel):
    ids: List[str|int] | None = None
    
class NewsUpdate(NewsBase):
    id: int

class NewsRead(NewsUpdate):
    # modify_date: datetime.datetime
    create_date: datetime.datetime
    

class NewsCreate(NewsBase):
    pass



class NewsList(BaseModel):
    total: int = 0
    list: List[NewsRead] = []