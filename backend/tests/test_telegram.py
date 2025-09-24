import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import zoneinfo
import os

from app.main import app
from app.database import Base, get_db
from app.utils.auth_utils import get_current_user

# Setup test DB
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


@pytest.fixture
def override_auth():
    class MockUser:
        id = 1
        username = "amen"
        email = "amen@example.com"
    app.dependency_overrides[get_current_user] = lambda: MockUser()
    yield
    app.dependency_overrides.pop(get_current_user, None)


API_VERSION = os.environ.get('API_VERSION')


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Mock authenticated user


def mock_user():
    class User:
        id = 1
    return User()

# Test registering a Telegram user


def test_register_telegram():
    payload = {"user_id": 1, "chat_id": "123456"}
    response = client.post(f"{API_VERSION}/telegram/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Registered successfully"
    assert data["chat_id"] == "123456"

# Test Telegram me


def test_get_my_telegram():
    response = client.get(f"{API_VERSION}/telegram/me")
    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == "123456"

# Test updating notification time


def test_update_notify_time():
    client.post(f"{API_VERSION}/telegram/register",
                json={"user_id": 1, "chat_id": "123456"})
    payload = {"notify_time": "09:30"}
    response = client.put(f"{API_VERSION}/telegram/time", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["notify_time"] == "09:30"


# Test connecting Telegram
def test_connect_telegram():
    response = client.post(f"{API_VERSION}/telegram/connect")
    assert response.status_code == 200
    assert "deep_link" in response.json()
    assert response.json()["deep_link"].startswith("https://t.me/")

# Test getting all Telegram users


def test_get_all_users():
    response = client.get(f"{API_VERSION}/telegram/all-users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["chat_id"] == "123456"

#  Test notify due (mocking the scraping function)


@patch("app.routes.appointments.scrape_appointments_playwright_sync")
def test_notify_due(mock_scrape):
    mock_scrape.return_value = [{"date": "2025-09-25", "location": "Berlin"}]

    # Set notify_time to current Berlin time
    now_str = datetime.now(zoneinfo.ZoneInfo(
        "Europe/Berlin")).strftime("%H:%M")
    client.put(f"{API_VERSION}/telegram/time", json={"notify_time": now_str})

    response = client.get(f"{API_VERSION}/telegram/notify-due?time={now_str}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "chat_id" in data[0]
    assert isinstance(data[0]["slots"], list)
