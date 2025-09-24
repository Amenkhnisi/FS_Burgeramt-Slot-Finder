from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.schemas import UserLogin, Token, UserCreate
from app import crud
from app.database import get_db
from app.utils.auth_utils import create_access_token, create_refresh_token
from fastapi.responses import JSONResponse
from app.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["Auth"])

# New endpoint to register


@router.post("/register", response_model=Token)
def register(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    existingU = crud.get_user_by_username(db, user_in.username)
    existingE = crud.get_user_by_email(db, user_in.email)
    if existingU:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    if existingE:
        raise HTTPException(
            status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in.username,
                            user_in.password, user_in.email)
    access_token = create_access_token({"sub": str(user.id)})
    # set HttpOnly cookie
    response.set_cookie(key="access_token", value=access_token,
                        httponly=True, samesite="lax")
    return {"access_token": access_token, "token_type": "bearer"}

# New endpoint to login


@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, user_in.username)
    if not user or not crud.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(
        {"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)}, expires_days=7)

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie("access_token", access_token, httponly=True,
                        secure=True, samesite="None", max_age=900)
    response.set_cookie("refresh_token", refresh_token, httponly=True,
                        secure=True, samesite="None", max_age=604800)
    return response

# New endpoint to logout


@router.post("/logout")
def logout(response: Response):
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token", path="/")
    # If using refresh tokens
    response.delete_cookie("refresh_token", path="/")
    return response

# New endpoint to refresh tokens


@router.post("/refresh")
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    print("Refresh token from cookie:", refresh_token)
    print(request.cookies.keys())  # Debug: print all cookie keys

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, JWT_SECRET,
                             algorithms=[JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(
        {"sub": str(user_id)})

    response = JSONResponse(content={"message": "Token refreshed"})
    response.set_cookie("access_token", new_access_token,
                        httponly=True, secure=True, samesite="Strict", max_age=900)
    return response
