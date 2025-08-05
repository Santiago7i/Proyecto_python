from typing import List, Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from enum import Enum

class CityEnum(str, Enum):
    bogota = "Bogotá"
    cartagena = "Cartagena"
    cali = "Cali"
    barranquilla = "Barranquilla"

class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    sede: CityEnum  # ennum para sede
    capacidad: int
    recursos: List[str] = Field(default_factory=list, sa_column=Column(JSON))
