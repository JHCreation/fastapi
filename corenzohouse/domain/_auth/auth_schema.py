from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional

class RefreshToken(BaseModel):
    refresh_token: str

class Token(BaseModel):
    access_token: str
    # token_type: str
    # userid: str
    refresh_token: Optional[str] = None 

class JWTpayload(BaseModel):
    userid: str
    usertype: str
    permission :str
    
class JWT(JWTpayload):
    exp: int
    