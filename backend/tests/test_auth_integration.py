from tests.utils import get_test_client
from datetime import datetime, timezone
from jose import jwt
import pytest
from fastapi.testclient import TestClient
from datetime import timedelta
from app.main import app
from app.utils.auth_utils import create_access_token, get_current_user
from app.models import User
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Clear any existing overrides to avoid conflicts
app.dependency_overrides.pop(get_current_user, None)

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

API_VERSION = os.environ.get('API_VERSION')


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def override_auth():
    class MockUser:
        id = 1
        username = "amen"
        email = "amen@example.com"
    app.dependency_overrides[get_current_user] = lambda: MockUser()
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    user = User(id=1, username="amen", email="amen@example.com",
                hashed_password="fakehash")
    db.add(user)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

# Test: Cookie-Based Access Token


def test_get_current_user_cookie(override_auth):
    token = create_access_token(
        {"sub": "1"}, expires_delta=timedelta(minutes=5))
    client.cookies.set("access_token", token)
    response = client.get(f"{API_VERSION}/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "amen"


# Test: Header-Based Access Token
def test_get_current_user_bearer():
    token = create_access_token(
        {"sub": "1"}, expires_delta=timedelta(minutes=5))
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{API_VERSION}/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "amen@example.com"


# Test: Missing Token
def test_get_current_user_missing_token():
    client = get_test_client(with_auth=False)
    response = client.get(f"{API_VERSION}/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# Test: Invalid Token
def test_get_current_user_invalid_token():
    client = get_test_client(with_auth=False)
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get(f"{API_VERSION}/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


# Test: Expired Token
JWT_SECRET = os.environ.get('JWT_SECRET')


def test_get_current_user_expired_token():
    client = get_test_client(with_auth=False)
    expired_payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
    }
    expired_token = jwt.encode(
        expired_payload, JWT_SECRET, algorithm="HS256")
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get(f"{API_VERSION}/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Access token expired"


def test_invalid_token_direct():
    from app.utils.auth_utils import get_current_user
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get(f"{API_VERSION}/users/me",
                          headers={"Authorization": "Bearer invalid.token"})
    print(response.status_code, response.json())
