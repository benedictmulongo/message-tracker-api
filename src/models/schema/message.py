from typing import List, Optional, Union
from pydantic import BaseModel, validator
from datetime import date, datetime
from .user import UserResponse, UserEmailRequest
import re

class UserMessageRequest(BaseModel):
    email_recipient: str
    subject: Optional[str]=None
    content: str
    @validator("email_recipient")
    def valid_email(cls, _email: str):
        pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        match = re.fullmatch(pattern, _email)
        if match is None:
            raise ValueError("Insert a valid e-mail")
        return _email

class UserMessageResponse(BaseModel):
    subject: str
    content: str
    is_fetched: bool
    send_date: datetime
    users: List[UserResponse]
    class Config():
        orm_mode = True


class MessageResponse(BaseModel):
    id: int
    subject: str
    content: str
    is_fetched: bool
    send_date: datetime
    users: List[UserEmailRequest]
    class Config():
        orm_mode = True

class MessagePaginateResponse(BaseModel):
    total: int
    hasNext: bool
    data: List[MessageResponse]
    class Config():
        orm_mode = True

class MultipleMessageRequest(BaseModel):
    ids: str
    # allOrNone: bool
    
    @validator("ids")
    def valid_id(cls, _ids: str):
        pattern = '[(\d+)(,)]+\d$'
        match = re.fullmatch(pattern, _ids)
        if match is None:
            raise ValueError("ids should be a succession of comma separated integers eg. ids=3,4,5,100")
        return _ids
