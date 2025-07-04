import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional
from typing import List, Any


class CategorysBase(BaseModel):
    key: str | None = None
    name: str | None = None
    value: Any | None = None
    status: str | None = None
    # modify_date: str | None = None
    # create_date: str | None = None
    user_id: int | None = None

class CategorysDelete(BaseModel):
    id: int

class CategorysDeletes(BaseModel):
    ids: str | None = None
    
class CategorysUpdate(CategorysBase):
    id: int

class CategorysRead(CategorysUpdate):
    modify_date: datetime.datetime
    create_date: datetime.datetime
    

class CategorysCreate(CategorysBase):
    pass



class CategorysList(BaseModel):
    total: int = 0
    list: List[CategorysRead] = []