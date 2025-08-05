import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends

load_dotenv()

db_username = os.getenv('USER_DB')
db_password = os.getenv('PASSWORD_DB')
db_host = os.getenv('HOST_DB')
db_name = os.getenv('NAME_DB')

url_connection = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:3306/{db_name}"
engine = create_engine(url_connection, echo=True)

def create_db_and_tables():
    from app.auth.model import User
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
