from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.utils.database import SessionDep
from app.models.reservation_model import Reservation
from app.models.room_model import Room
from app.auth.dependencies import admin_required

router = APIRouter(prefix="/reports", tags=["Reports"])

# 1 slala mas reservada
@router.get("/most-booked-room")
def most_booked_room(session: SessionDep, user=Depends(admin_required)):
    result = (
        session.query(
            Room.nombre,
            func.count(Reservation.id).label("total_reservas")
        )
        .join(Reservation, Reservation.room_id == Room.id)
        .group_by(Room.id)
        .order_by(func.count(Reservation.id).desc())
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No hay reservas registradas...")
    return {"sala": result[0], "reservas": result[1]}

# 2. Total de horas reservadas por un usuario en el mes de ahorita
@router.get("/user-hours/{user_id}")
def user_hours_this_month(user_id: int, session: SessionDep, user=Depends(admin_required)):
    today = datetime.today()
    year = today.year
    month = today.month

    reservas = (
        session.query(Reservation)
        .filter(
            Reservation.user_id == user_id,
            extract("year", Reservation.fecha) == year,
            extract("month", Reservation.fecha) == month,
            Reservation.estado == "confirmada"  # Solo confirmadas cuentan
        )
        .all()
    )

    total_horas = 0
    for r in reservas:
        duracion = datetime.combine(r.fecha, r.hora_fin) - datetime.combine(r.fecha, r.hora_inicio)
        total_horas += duracion.total_seconds() / 3600  # convertir a horas

    return {
        "usuario_id": user_id,
        "mes": f"{year}-{month:02}",
        "total_horas": total_horas
    }
