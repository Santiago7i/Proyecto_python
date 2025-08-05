from fastapi import FastAPI
from app.utils.database import create_db_and_tables
from app.auth.controller import router as auth_router
from app.routes.room_routes import router as room_router
from app.routes.user_routes import router as user_router
from app.routes.reservation_routes import router as reservation_router
from app.routes.report_routes import router as report_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)
app.include_router(room_router)
app.include_router(user_router)
app.include_router(reservation_router)
app.include_router(report_router)
