from fastapi import APIRouter, Depends, HTTPException
from app.utils.database import SessionDep
from app.models.reservation_model import Reservation
from app.schemas.reservation_schema import ReservationCreate, ReservationRead
from app.auth.dependencies import get_current_user
from sqlmodel import select, and_
from typing import List
from datetime import date, datetime, timedelta

router = APIRouter(prefix="/reservations", tags=["Reservations"])

# Crear reserva para el tema de 1 hora exacta y sin cruce de horarios
@router.post("/", response_model=ReservationRead)
def create_reservation(data: ReservationCreate, session: SessionDep, user=Depends(get_current_user)):
    # Validamo que la duracion sea exactamente 1 hora
    inicio_dt = datetime.combine(data.fecha, data.hora_inicio)
    fin_dt = datetime.combine(data.fecha, data.hora_fin)
    if fin_dt - inicio_dt != timedelta(hours=1):
        raise HTTPException(status_code=400, detail="La reserva debe durar exactamente 1 hora")

    # Validamos que no haya cruce de horarios en la misma sala
    overlapping = session.exec(
        select(Reservation).where(
            Reservation.room_id == data.room_id,
            Reservation.fecha == data.fecha,
            Reservation.estado != "cancelada",
            and_(
                Reservation.hora_inicio < data.hora_fin,
                Reservation.hora_fin > data.hora_inicio
            )
        )
    ).first()

    if overlapping:
        raise HTTPException(status_code=400, detail="Ya existe una reserva para esa sala en ese horario")

    # Creamos reserva con estado por defecto "pendiente"
    reserva = Reservation(
        user_id=user.id,
        room_id=data.room_id,
        fecha=data.fecha,
        hora_inicio=data.hora_inicio,
        hora_fin=data.hora_fin,
        estado="pendiente"
    )
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva

# Consultar mis reservas
@router.get("/me", response_model=List[ReservationRead])
def get_my_reservations(session: SessionDep, user=Depends(get_current_user)):
    return session.exec(select(Reservation).where(Reservation.user_id == user.id)).all()

# Consultar reservas por sala
@router.get("/room/{room_id}", response_model=List[ReservationRead])
def get_by_room(room_id: int, session: SessionDep):
    return session.exec(select(Reservation).where(Reservation.room_id == room_id)).all()

# Consultar reservas por fecha
@router.get("/date/{res_date}", response_model=List[ReservationRead])
def get_by_date(res_date: date, session: SessionDep):
    return session.exec(select(Reservation).where(Reservation.fecha == res_date)).all()

# Cancelar reserva (ojo solo el dueño puede hacer esto )
@router.delete("/{reservation_id}")
def cancel_reservation(reservation_id: int, session: SessionDep, user=Depends(get_current_user)):
    reserva = session.get(Reservation, reservation_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada...")

    if reserva.user_id != user.id:
        raise HTTPException(status_code=403, detail="No puedes cancelar esta reserva...")

    reserva.estado = "cancelada"
    session.commit()
    return {"message": "Reserva cancelada"}
