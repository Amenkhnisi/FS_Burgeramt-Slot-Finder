from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.utils.oauth_utils import get_user_from_oauth
from app.utils.auth_utils import create_access_token
from app import crud
from app.database import get_db
import os


router = APIRouter(prefix="/oauth", tags=["OauthV2"])

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


@router.get("/google/callback")
def google_callback(code: str, response: Response, db: Session = Depends(get_db)):
    # ✅ Exchange Google code for user info

    user_info = get_user_from_oauth(
        provider="google",
        code=code,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=f"{FRONTEND_URL}/oauth/callback",
    )

    if not user_info.get("email"):
        raise HTTPException(
            status_code=400, detail="Google login failed: no email returned")

    # Find or create user
    user = crud.get_user_by_email(db, user_info["email"])
    if not user:
        user = crud.create_user(
            db, username=user_info["username"], password=None, email=user_info["email"])

    # Create token
    access_token = create_access_token({"sub": str(user.id)})

    # ✅ Set secure HttpOnly cookie (cross-origin friendly)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",   # use "lax" for localhost dev
        secure=False,     # must be False for http
        path="/"
    )

    # **Important: cross-site cookies**
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",  # use 'none' if frontend is on a different domain
        secure=False,     # True if using HTTPS
        max_age=3600*24
    )

    return {"msg": "Login successful"}


""" @router.get("/github/callback")
def github_callback(code: str, response: Response, db: Session = Depends(get_db)):
    user_info = get_user_from_oauth(
        provider="github",
        code=code,
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        redirect_uri=f"{BACKEND_URL}/oauth/github/callback",
    )

    if not user_info.get("email"):
        raise HTTPException(
            status_code=400, detail="GitHub login failed: no email returned")

    # Find or create user
    user = crud.get_user_by_email(db, user_info["email"])
    if not user:
        user = crud.create_user(
            db, username=user_info["username"], password=None, email=user_info["email"])

    # Create token
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token,
                        httponly=True, samesite="lax")

    return RedirectResponse(f"{FRONTEND_URL}/dashboard") """
