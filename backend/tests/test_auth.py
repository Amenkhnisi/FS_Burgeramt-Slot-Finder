import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app  # adjust import to your FastAPI app
from app.database import Base, get_db
import os


# Create a test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Override DB dependency


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Registration Tests

API_VERSION = os.environ.get('API_VERSION')


def test_register_success():
    response = client.post(f"{API_VERSION}/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert response.cookies.get("access_token") is not None


def test_register_duplicate_username():
    client.post(f"{API_VERSION}/auth/register", json={
        "username": "dupeuser",
        "email": "dupe@example.com",
        "password": "pass"
    })
    response = client.post(f"{API_VERSION}/auth/register", json={
        "username": "dupeuser",
        "email": "new@example.com",
        "password": "pass"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_register_duplicate_email():
    client.post(f"{API_VERSION}/auth/register", json={
        "username": "newuser",
        "email": "dupeemail@example.com",
        "password": "pass"
    })
    response = client.post(f"{API_VERSION}/auth/register", json={
        "username": "anotheruser",
        "email": "dupeemail@example.com",
        "password": "pass"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


# Login Tests

def test_login_success():
    client.post(f"{API_VERSION}/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass"
    })
    response = client.post(f"{API_VERSION}/auth/login", json={
        "username": "loginuser",
        "password": "loginpass"
    })
    assert response.status_code == 200
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None


def test_login_failure():
    response = client.post(f"{API_VERSION}/auth/login", json={
        "username": "wronguser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


# Logout Tests

def test_logout():
    response = client.post(f"{API_VERSION}/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None
    # Ensure cookies are deleted
    assert response.headers.get("set-cookie") is not None

# Token Refresh Tests


def test_refresh_token_flow():
    # Register and login
    client.post(f"{API_VERSION}/auth/register", json={
        "username": "refreshuser",
        "email": "refresh@example.com",
        "password": "refreshpass"
    })
    login_response = client.post(f"{API_VERSION}/auth/login", json={
        "username": "refreshuser",
        "password": "refreshpass"
    })
    refresh_token = login_response.cookies.get("refresh_token")
    assert refresh_token is not None

    # Refresh
    client.cookies.set("refresh_token", refresh_token)
    response = client.post(f"{API_VERSION}/auth/refresh")
    assert response.status_code == 200
    assert response.json()["message"] == "Token refreshed"
    assert response.cookies.get("access_token") is not None
