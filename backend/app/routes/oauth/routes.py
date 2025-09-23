from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os

router = APIRouter(prefix="/oauth", tags=["Oauth"])

FRONTEND_URL = os.getenv("FRONTEND_URL")
BACKEND_URL = os.getenv("BACKEND_URL")

GOOGLE_CLIENT_ID = os.getenv(
    "GOOGLE_CLIENT_ID")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID ")

# 🔹 Step 1: Redirect to Google login


@router.get("/google")
def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={BACKEND_URL}/oauth/google/callback"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
    )
    return RedirectResponse(google_auth_url)


# 🔹 Step 1: Redirect to GitHub login
@router.get("/github")
def github_login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={BACKEND_URL}/oauth/github/callback"
        "&scope=user:email"
    )
    return RedirectResponse(github_auth_url)
