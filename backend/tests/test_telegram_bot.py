import pytest
from unittest.mock import patch, MagicMock
from app.services.telegram_bot import send_message, get_updates, process_updates


@pytest.fixture
def mock_chat_id():
    return "123456789"


@pytest.fixture
def mock_text():
    return "Hello, Amen!"


def test_send_message(mock_chat_id, mock_text):
    with patch("app.services.telegram_bot.requests.post") as mock_post:
        send_message(mock_chat_id, mock_text)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "sendMessage" in args[0]
        assert kwargs["data"]["chat_id"] == mock_chat_id
        assert kwargs["data"]["text"] == mock_text


def test_get_updates_no_offset():
    mock_response = {"result": [{"update_id": 1, "message": {
        "chat": {"id": "123"}, "text": "/start uid_1"}}]}
    with patch("app.services.telegram_bot.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        updates = get_updates()
        assert isinstance(updates, list)
        assert updates[0]["message"]["text"].startswith("/start")


def test_get_updates_with_offset():
    mock_response = {"result": [{"update_id": 2}]}
    with patch("app.services.telegram_bot.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        updates = get_updates(offset=2)
        mock_get.assert_called_once()
        assert updates[0]["update_id"] == 2


def test_process_updates_valid_user():
    mock_update = {
        "message": {
            "chat": {"id": "123"},
            "text": "/start uid_42"
        }
    }

    mock_user = MagicMock()
    mock_user.telegram_chat_id = None

    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = mock_user

    with patch("app.services.telegram_bot.get_updates", return_value=[mock_update]), \
            patch("app.services.telegram_bot.SessionLocal", return_value=mock_db), \
            patch("app.services.telegram_bot.send_message") as mock_send:

        process_updates()
        mock_db.commit.assert_called_once()
        mock_send.assert_called_once_with(
            "123", "✅ Connected! You'll now receive daily appointment notifications.")


def test_process_updates_invalid_user():
    mock_update = {
        "message": {
            "chat": {"id": "123"},
            "text": "/start uid_999"
        }
    }

    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None

    with patch("app.services.telegram_bot.get_updates", return_value=[mock_update]), \
            patch("app.services.telegram_bot.SessionLocal", return_value=mock_db), \
            patch("app.services.telegram_bot.send_message") as mock_send:

        process_updates()
        mock_send.assert_called_once_with(
            "123", "⚠️ Invalid link, please try again.")
