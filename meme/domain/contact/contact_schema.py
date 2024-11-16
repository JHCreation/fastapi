import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
# from pydantic.main import 
from typing import Optional
from typing import List

class Contact(BaseModel):
    key: str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    content: str | None = None
    # doc_01: str | None = None
    # doc_02: str | None = None
    # create_date: datetime.datetime

class ContactDelete(BaseModel):
    id: int

class ContactDeletes(BaseModel):
    ids: str | None = None
    
class ContactUpdate(Contact):
    id: int



class ContactRead(ContactUpdate):
    # modify_date: datetime.datetime
    create_date: datetime.datetime
    

class ContactCreate(Contact):
    pass



class ContactList(BaseModel):
    total: int = 0
    list: List[ContactRead] = []