import pytest
from unittest.mock import MagicMock
from app import crud
from app import models


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_user():
    return models.User(id=1, username="amen", email="amen@example.com", hashed_password="hashed")


def test_get_user_by_username(mock_db, mock_user):
    mock_db.query().filter().first.return_value = mock_user
    result = crud.get_user_by_username(mock_db, "amen")
    assert result.username == "amen"


def test_get_user_by_email(mock_db, mock_user):
    mock_db.query().filter().first.return_value = mock_user
    result = crud.get_user_by_email(mock_db, "amen@example.com")
    assert result.email == "amen@example.com"


def test_get_user_by_id(mock_db, mock_user):
    mock_db.query().get.return_value = mock_user
    result = crud.get_user_by_id(mock_db, 1)
    assert result.id == 1


def test_create_user(mock_db):
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    user = crud.create_user(
        mock_db, "newuser", "password123", "new@example.com")
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.hashed_password != "password123"  # should be hashed


def test_verify_password():
    plain = "password123"
    hashed = crud.pwd_context.hash(plain)
    assert crud.verify_password(plain, hashed)


def test_get_telegram_user(mock_db):
    mock_tg_user = models.TelegramUser(
        user_id=1, chat_id="12345", notify_time="08:00")
    mock_db.query().filter().first.return_value = mock_tg_user
    result = crud.get_telegram_user(mock_db, 1)
    assert result.chat_id == "12345"


def test_create_telegram_user(mock_db):
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    tg_user = crud.create_telegram_user(mock_db, 1, "12345", "08:00")
    assert tg_user.user_id == 1
    assert tg_user.chat_id == "12345"
    assert tg_user.notify_time == "08:00"


def test_update_notify_time_success(mock_db):
    mock_tg_user = models.TelegramUser(
        user_id=1, chat_id="12345", notify_time="08:00")
    mock_db.query().filter().first.return_value = mock_tg_user
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    updated = crud.update_notify_time(mock_db, 1, "09:00")
    assert updated.notify_time == "09:00"


def test_update_notify_time_failure(mock_db):
    mock_db.query().filter().first.return_value = None
    result = crud.update_notify_time(mock_db, 999, "09:00")
    assert result == {"error": "User not found"}
