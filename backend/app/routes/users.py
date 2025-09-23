from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.auth_utils import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}
