import pytest
from aiogram import Dispatcher, types
from aiogram.types import Chat, User, Message, Update
from unittest.mock import patch, MagicMock, AsyncMock


# Import the handler to be tested
from handlers.start import register_start_handler


@pytest.mark.asyncio
async def test_cmd_start_with_valid_uid():
    dp = Dispatcher()

    register_start_handler(dp)

    fake_user = User(id=111, is_bot=False, first_name="Test")
    fake_chat = Chat(id=222, type="private")

    message = Message(
        message_id=1,
        date="2024-09-23",
        chat=fake_chat,
        from_user=fake_user,
        text="/start uid_123"
    )
    update = Update(update_id=999, message=message)

    with (
        patch("handlers.start.requests.post") as mock_post,
        patch.object(Message, "answer", new_callable=AsyncMock) as mock_answer,
    ):
        mock_post.return_value.ok = True

        # instead of real bot, pass a MagicMock
        bot = MagicMock()

        await dp.feed_update(bot, update)

        # Ensure backend call
        args, kwargs = mock_post.call_args
        assert kwargs["json"] == {"user_id": "123", "chat_id": "222"}

        # Ensure reply
        mock_answer.assert_awaited_with(
            "✅ Your Telegram is now connected! You will receive daily appointment alerts.")


@pytest.mark.asyncio
async def test_cmd_start_without_uid():
    dp = Dispatcher()

    register_start_handler(dp)

    fake_user = User(id=333, is_bot=False, first_name="Test2")
    fake_chat = Chat(id=444, type="private")

    message = Message(
        message_id=2,
        date="2024-09-23",
        chat=fake_chat,
        from_user=fake_user,
        text="/start"
    )
    update = Update(update_id=1000, message=message)

    with patch.object(Message, "answer", new_callable=AsyncMock) as mock_answer:
        bot = MagicMock()
        await dp.feed_update(bot, update)

        mock_answer.assert_awaited_with(
            "👋 Welcome to Bürgeramt Slot Finder!\n\n"
            "Please connect your account from the app using the 'Connect Telegram' button."
        )
