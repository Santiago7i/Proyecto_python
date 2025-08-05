from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user, admin_required
from app.auth.model import User
from app.utils.database import SessionDep
from typing import List
from app.auth.schemas import UserCreate, UserLogin, TokenResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserCreate])
def get_users(session: SessionDep, _: User = Depends(admin_required)):
    return session.query(User).all()

@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep, _: User = Depends(admin_required)):
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(user)
    session.commit()
    return {"message": "Usuario eliminado correctamente"}
