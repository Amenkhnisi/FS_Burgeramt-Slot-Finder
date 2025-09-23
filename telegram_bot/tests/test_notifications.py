import pytest
from unittest.mock import patch, AsyncMock
from notifications import send_daily_notifications
from config import Settings

settings = Settings()


@pytest.mark.asyncio
async def test_send_daily_notifications_success():
    bot = AsyncMock()

    mock_response = {
        "chat_id": "12345",
        "slots": [
            {"date": "2025-09-23", "label": "Mitte", "link": "https://example.com"}
        ]
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = [mock_response]

        job = send_daily_notifications(bot, settings)
        await job()

        bot.send_message.assert_called_once()
