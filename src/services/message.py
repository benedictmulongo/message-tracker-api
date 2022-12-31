from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from src.models.schema.user import UserResponse, UserRequest
from src.models.data.tracker import User
from src.database.connector import get_db
from src.repository.message import MessageRepository
from typing import Optional, List
from sqlalchemy.orm import Session
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status, HTTPException
from src.models.data.tracker import User, Message
from src.database.connector import get_db
from fastapi.encoders import jsonable_encoder
from src.models.schema.message import UserMessageRequest
from datetime import datetime
from typing import Tuple
from src.database.connector import get_db
from .dependency import Pagination, SortDirection

pagination = Pagination(maximum_limit=5)

class MessageService: 
    
    def __init__(self, session: Session):
        self.repository: MessageRepository = MessageRepository(session)
    
    def send_message(self, request: UserMessageRequest):
        recipient = self.repository.get_recipient_or_404(request.email_recipient)
        msg = Message(
            subject=request.subject, 
            content=request.content,
            is_fetched=False,
            send_date=datetime.now())
        msg.users.append(recipient)
        self.repository.insert_message(msg)
        return msg

    def fetch_all_msgs(self, page: Tuple[SortDirection,int, int] = Depends(pagination.page_size)):
        sort_direction, page_number, page_size = page
        offset_index = (page_number-1)*page_size
        (messages, total, num_pages) = self.repository.get_paginated_messages(
            sortDir=sort_direction, size=page_size, offset_index=offset_index)
        response = {}
        response["total"] = total
        response["hasNext"] = True if page_number <= num_pages else False
        response["data"] = messages
        msg_ids = [msg.id for msg in messages]
        # Consider those messages as fetched
        self.repository.set_all_messages_to_fetched_by_ids(msg_ids)
        return response

    @staticmethod
    def fetch_all_msgs_static(page: Tuple[SortDirection,int, int] = Depends(pagination.page_size),
    db: Session = Depends(get_db)):
        repository: MessageRepository = MessageRepository(db)
        sort_direction, page_number, page_size = page
        offset_index = (page_number-1)*page_size
        (messages, total, num_pages) = repository.get_paginated_messages(
            sortDir=sort_direction, size=page_size, offset_index=offset_index)
        response = {}
        response["total"] = total
        response["hasNext"] = True if page_number <= num_pages else False
        response["data"] = messages
        msg_ids = [msg.id for msg in messages]
        # Consider those messages as fetched
        yield response
        repository.set_all_messages_to_fetched_by_ids(msg_ids)

    @staticmethod
    def fetch_new_msgs_static(db: Session = Depends(get_db)):
        repository: MessageRepository = MessageRepository(db)
        messages = repository.get_all_unfetched_messages()
        msg_ids = [msg.id for msg in messages]
        yield messages
        # Consider those messages as fetched
        repository.set_all_messages_to_fetched_by_ids(msg_ids)

    def delete_multiple_msg_by_id(self, ids: str):
        """
            This function finds the subset of IDs from input: ids
            who also exist in the database. That subset if found
            by computing the intersection between db.ids and input.ids
            if diff = 0 => all values in ids exist in database
            if intersect = 0 => all values does not exist
            if intersect != 0 & allOrNone=true => exception
            if intersect != 0 & allOrNone=False 
                => delete_multiple_messages_by_ids(intersect.ids)
            Here we are computing from the "allOrNone=False" point of vue
        """
        all_msgs: List = self.repository.get_all_messages()
        db_ids = {x.id for x in all_msgs}
        requested_ids = {int(x) for x in ids.split(',')}
        intersect = db_ids.intersection(requested_ids)
        diff = requested_ids.difference(db_ids)
        print("intersection:", intersect) # case allOrNone=False
        print("difference:", requested_ids.difference(db_ids)) # if diff=0, all values exist, else those values does not exist
        valid_ids = list(intersect)
        if len(valid_ids) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Messages with ids {requested_ids} does not exist")
        self.repository.delete_multiple_messages_by_ids(valid_ids)
        # return valid_ids