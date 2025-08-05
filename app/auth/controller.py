from fastapi import APIRouter, HTTPException, status
from app.utils.database import SessionDep
from app.auth.model import User
from app.auth.schemas import UserCreate, UserLogin, TokenResponse
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, session: SessionDep):
    existing = session.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    token = create_access_token({"sub": db_user.email})
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, session: SessionDep):
    user = session.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": user.email, "role": user.role})
    return TokenResponse(access_token=token)

