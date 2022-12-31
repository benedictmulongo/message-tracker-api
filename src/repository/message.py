from typing import Dict, Any
from fastapi import APIRouter, Depends, Response, status, HTTPException
from src.models.data.tracker import User, Message
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, query
from typing import Optional, List
from sqlalchemy import and_, or_, not_
from src.models.schema.user import UserRequestUpdatable

class MessageRepository: 
    
    def __init__(self, session: Session):
        self.db: Session = session
    
    def get_message_query_or_404(self, id: int) -> query.Query:
        msg = self.db.query(Message).filter(Message.id==id)
        if not msg.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with id {id} does not exist--")
        return msg

    def get_recipient_query_or_404(self, email_recipient: str) -> query.Query:
        current_user = self.db.query(User).filter(User.email==email_recipient)
        if not current_user.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Recipient with email {email_recipient} does not exist")
        return current_user

    def get_recipient_or_404(self, email_recipient: str) -> User:
        current_user = self.db.query(User).filter(User.email==email_recipient)
        if not current_user.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Recipient with email {email_recipient} does not exist")
        return current_user.first()

    def insert_message(self, msg: Message) -> bool: 
        try:
            self.db.add(msg)
            self.db.commit()
        except: 
            return False 
        return True

    def get_all_messages(self):
        msgs = self.db.query(Message).all()
        return msgs

    def get_message_by_id(self, id: int) -> Message:
        msg = self.get_message_query_or_404(id)
        return msg.first()

    def get_paginated_messages(self, sortDir: str, size: int, offset_index: int):
        msq_query = self.db.query(Message)
        total = msq_query.count()
        num_pages = total // size
        if sortDir == "asc":
            msgs = msq_query.order_by(Message.send_date.asc()).limit(size).offset(offset_index).all()
            return (msgs, total, num_pages)
        msgs = msq_query.order_by(Message.send_date.desc()).limit(size).offset(offset_index).all()
        return (msgs, total, num_pages)

    def set_all_messages_to_fetched_by_ids(self, msg_ids: List[int]):
        self.db.query(Message).filter(and_(Message.id.in_(msg_ids), Message.is_fetched==False)).update(
                {Message.is_fetched:True}, 
                synchronize_session = False)
        self.db.commit()

    def get_all_unfetched_messages(self):
        msg_query = self.db.query(Message)
        messages  = msg_query.order_by(Message.send_date.desc()).filter(Message.is_fetched==False).all()
        return messages


    def delete_message_by_id(self, id:int) -> bool: 
        _msg = self.get_message_query_or_404(id)
        try:
            _msg.delete(synchronize_session=False)
            self.db.commit()
        except: 
            return False 
        return True

    def delete_multiple_messages_by_ids(self, msg_ids: List[int]):
        msgs = self.db.query(Message).filter(Message.id.in_(msg_ids))
        msgs.delete(synchronize_session=False)
        self.db.commit()
