import datetime
from pydantic import BaseModel, ConfigDict, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional
from typing import List


class WorksBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    key: str | None = None
    title: str | None = None
    subject: str | None = None
    contents: str | None = None
    images: list | None = None
    public: str | None = None

class WorksDelete(BaseModel):
    id: int

class WorksDeletes(BaseModel):
    ids: List[str|int] | None = None
    
class WorksUpdate(WorksBase):
    id: int

class WorksRead(WorksUpdate):
    # modify_date: datetime.datetime
    create_date: datetime.datetime
    

class WorksCreate(WorksBase):
    pass



class WorksList(BaseModel):
    total: int = 0
    list: List[WorksRead] = []