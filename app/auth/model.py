from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password: str
    role: str

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"