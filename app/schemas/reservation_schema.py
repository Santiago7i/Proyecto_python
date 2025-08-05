from typing import Optional
from pydantic import BaseModel
from datetime import date, time

class ReservationBase(BaseModel):
    fecha: date
    hora_inicio: time
    hora_fin: time

class ReservationCreate(ReservationBase):
    room_id: int

class ReservationRead(ReservationBase):
    id: int
    room_id: int
    user_id: int
    estado: str 

    class Config:
        orm_mode = True
