from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from app.auth.model import User
from app.auth.schemas import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.database import SessionDep

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
def register_user(user: UserCreate, session: SessionDep):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya esta registrado...")

    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"msg": "Usuario registrado correctamente", "user_id": db_user.id}

@router.post("/login")
def login_user(user: UserLogin, session: SessionDep):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales no correctas...")

    token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
