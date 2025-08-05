from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.room_model import Room
from app.schemas.room_schema import RoomCreate, RoomUpdate

def get_rooms(session: Session):
    return session.exec(select(Room)).all()

def create_room(data: RoomCreate, session: Session):
    room = Room(**data.dict())
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

def update_room(room_id: int, data: RoomUpdate, session: Session):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada...")
    
    room_data = data.dict(exclude_unset=True)
    for key, value in room_data.items():
        setattr(room, key, value)

    session.add(room)
    session.commit()
    session.refresh(room)
    return room

def delete_room(room_id: int, session: Session):
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada...")

    session.delete(room)
    session.commit()
    return {"msg": "Sala eliminada"}
