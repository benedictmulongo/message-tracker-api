from typing import List, Optional
from pydantic import BaseModel, validator
import re

class UserRequest(BaseModel):
    fullname: str
    username: str
    email: str
    phone_number: str
    @validator("email")
    def valid_email(cls, _email: str):
        pattern = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        match = re.fullmatch(pattern, _email)
        if match is None:
            raise ValueError("Insert a valid e-mail")
        return _email

class UserResponse(BaseModel): # Response model - DTO - data transfer object
    username: str
    email: str
    phone_number: str
    class Config():
        orm_mode = True

class UserRequestUpdatable(BaseModel):
    fullname: Optional[str]=None
    username: Optional[str]=None
    email: Optional[str]=None
    phone_number: Optional[str]=None

class UserEmailRequest(BaseModel):
    email: str
    @validator("email")
    def valid_email(cls, _email: str):
        pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        match = re.fullmatch(pattern, _email)
        if match is None:
            raise ValueError("Insert a valid e-mail")
        return _email
    class Config():
        orm_mode = True
