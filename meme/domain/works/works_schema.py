import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional
from typing import List

class Works(BaseModel):
    key: str | None = None
    title: str | None = None
    content: str | None = None
    # doc_01: str | None = None
    # doc_02: str | None = None
    # create_date: datetime.datetime

class WorksDelete(BaseModel):
    id: int

class WorksDeletes(BaseModel):
    ids: str | None = None
    
class WorksUpdate(Works):
    id: int



class WorksRead(WorksUpdate):
    # modify_date: datetime.datetime
    create_date: datetime.datetime
    

class WorksCreate(Works):
    pass



class WorksList(BaseModel):
    total: int = 0
    list: List[WorksRead] = []