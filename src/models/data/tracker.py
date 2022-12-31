from operator import index
import datetime
from sqlalchemy import Table, Column, String, MetaData, Integer, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.connector import Base

association_table = Table(
    "user_message",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("message_id", ForeignKey("message.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    fullname =  Column(String)
    username =  Column(String, unique=True)
    email =  Column(String, unique=True)
    phone_number =  Column(String, unique=True)
    messages = relationship("Message", cascade="all, delete", secondary=association_table, back_populates="users")
    
    def __init__(self, fullname,username,email,phone_number):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return f"User[username:{self.username}, email:{self.email}, phone_number:{self.phone_number}, msgs:{self.messages}]"


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    subject =  Column(Text)
    content =  Column(Text)
    is_fetched = Column(Boolean, default=False) # set default=false
    send_date = Column(DateTime(timezone=True), server_default=func.now())
    users = relationship("User", cascade="all, delete", secondary=association_table, back_populates="messages")
    
    def __init__(self, subject, content, is_fetched = False, send_date= func.now()):
        self.subject = subject
        self.content = content
        self.is_fetched = is_fetched
        self.send_date = send_date

    def __repr__(self):
        return f"Msg[subject:{self.subject}, content:{self.content}, user:{self.users}]"
