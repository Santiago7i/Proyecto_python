from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, time

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="room.id")
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str = Field(default="pendiente")  # se deja el valor por fdefecto
