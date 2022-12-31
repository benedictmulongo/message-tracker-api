from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, String, MetaData, select
from sqlalchemy.orm import sessionmaker, scoped_session
from os import environ
from pathlib import Path
import sys
import os

dbDir = os.path.join(os.path.dirname(__file__), "message-tracker-database.db") # use realtive path
# SQLALCHEMY_DATABASE_URI = 'sqlite:///./blog.db' # environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbDir
SQLALCHEMY_ENGINE_OPTIONS = {
    'check_same_thread': False
    } 
SQLALCHEMY_TRACK_MODIFICATIONS = False
#  SQLALCHEMY_DATABASE_SCHEMA = environ.get('SQLALCHEMY_DATABASE_SCHEMA')
db_engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args=SQLALCHEMY_ENGINE_OPTIONS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

event.listen(db_engine, 'connect', _fk_pragma_on_connect)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_concrete():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def random_file_hint():
    dbDir = os.path.join(os.path.dirname(__file__), "blog.db")
    print("os.path.dirname(__file__)=", os.path.dirname(__file__))
    base_path = Path(__file__).parent
    print("base_path:")
    print(base_path)
    print("dbDir:")
    print(dbDir)
    file_path = (base_path / "gcodes/start.gcode").resolve()
    print("file_path:")
    print(file_path)

