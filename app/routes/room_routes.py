from fastapi import APIRouter, Depends, HTTPException
from app.models.room_model import Room
from app.utils.database import SessionDep
from app.auth.dependencies import get_current_user, admin_required
from app.schemas.room_schema import RoomCreate, RoomRead, RoomUpdate
from typing import List

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("/", response_model=List[RoomRead])
def get_rooms(session: SessionDep):
    return session.query(Room).all()

@router.post("/", response_model=RoomRead)
def create_room(room: RoomCreate, session: SessionDep, user=Depends(admin_required)):
    new_room = Room.from_orm(room)
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    return new_room

@router.put("/{room_id}", response_model=RoomRead)
def update_room(room_id: int, room: RoomUpdate, session: SessionDep, user=Depends(admin_required)):
    db_room = session.query(Room).get(room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Sala no encontrada...")
    for key, value in room.dict(exclude_unset=True).items():
        setattr(db_room, key, value)
    session.commit()
    session.refresh(db_room)
    return db_room

@router.delete("/{room_id}")
def delete_room(room_id: int, session: SessionDep, user=Depends(admin_required)):
    db_room = session.query(Room).get(room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Sala no encontrada...")
    session.delete(db_room)
    session.commit()
    return {"message": "Sala eliminada correctamente"}
