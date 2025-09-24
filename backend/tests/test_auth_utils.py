from app.utils.auth_utils import create_access_token, create_refresh_token
from datetime import timedelta
from jose import jwt
import os


JWT_SECRET = os.environ.get('JWT_SECRET')


def test_create_access_token():
    token = create_access_token(
        {"sub": "123"}, expires_delta=timedelta(minutes=5))
    decoded = jwt.decode(token, {JWT_SECRET}, algorithms=["HS256"])
    assert decoded["sub"] == "123"
    assert "exp" in decoded


def test_create_refresh_token():
    token = create_refresh_token({"sub": "456"}, expires_days=1)
    decoded = jwt.decode(token, {JWT_SECRET}, algorithms=["HS256"])
    assert decoded["sub"] == "456"
    assert "exp" in decoded
