from typing import Dict, Any
from fastapi import APIRouter, Depends, Response, status, HTTPException
from src.models.data.tracker import User, Message
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, query
from src.models.schema.user import UserRequestUpdatable

class UserRepository: 
    
    def __init__(self, session: Session):
        self.db: Session = session
    
    def get_user_query_or_404(self, id: int) -> query.Query:
        current_user = self.db.query(User).filter(User.id==id)
        if not current_user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist--")
        return current_user

    def insert_user(self, usr: User) -> bool: 
        try:
            self.db.add(usr)
            self.db.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "msg": f"All parameters should be unique, user with same parameters already exist",
                "cause": f"{str(e.orig)}",
                "params": f"{list(e.params)}"
            }) 
        except: 
            return False 
        return True

    def get_all_users(self):
        users  = self.db.query(User).all()
        return users

    def get_user_by_id(self, id:int): 
        # self.db.query(User).filter(User.id==id).one_or_none()
        current_user = self.get_user_query_or_404(id)
        return current_user.first()

    def delete_user(self, id:int) -> bool: 
        current_user = self.get_user_query_or_404(id)
        try:
            current_user.delete(synchronize_session=False)
            self.db.commit()
        except: 
            return False 
        return True

    def update_user(self, id:int, request:UserRequestUpdatable) -> bool: # schema
        current_user = self.get_user_query_or_404(id)
        try:
            updated_keys = request.dict(exclude_unset=True)
            current_user.update(updated_keys)
            # db.refresh(current_user)
            self.db.commit()
            return current_user
        except: 
            return False

    def create_or_overwrite_if_exist(self, id:int, request:Dict[str, Any]) -> bool: 
        #return user.put_overwrite_if_exist(id, request, db)
        # PUT ===> for checking if resource exists then update, else create new resource
        current_user = self.db.query(User).filter(User.id==id)
        try:
        
            if not current_user.first():
                return self.insert_user(request)
            update_key = jsonable_encoder(request)
            current_user.update(update_key)
            self.db.commit()
        except: 
            return False 
        return True
    
    