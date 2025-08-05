from typing import Optional, List
from sqlmodel import SQLModel
from app.models.room_model import CityEnum

class RoomBase(SQLModel):
    nombre: str
    sede: CityEnum
    capacidad: int
    recursos: List[str]

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id: int

class RoomUpdate(SQLModel):
    nombre: Optional[str] = None
    sede: Optional[CityEnum] = None
    capacidad: Optional[int] = None
    recursos: Optional[List[str]] = None
