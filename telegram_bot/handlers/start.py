import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import zoneinfo
from config import Settings

settings = Settings()


# ==============================
# Config
# ==============================
TELEGRAM_BOT_TOKEN = settings.telegram_bot_token
API_VERSION = settings.api_version
API_BASE = settings.api_base + "/" + API_VERSION
# For local testing with backend on localhost, use:
# API_BASE = "http://localhost:8000/" + API_VERSION


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
scheduler = AsyncIOScheduler()


# ==============================
# Handlers
# ==============================
def register_start_handler(dp: Dispatcher):

    @dp.message(CommandStart())
    async def cmd_start(message: types.Message):
        """
        Handle /start with deep link: /start uid_{userId}
        Example: /start uid_42
        """
        args = message.text.split(" ")

        if len(args) > 1 and args[1].startswith("uid_"):
            user_id = args[1].replace("uid_", "")
            chat_id = message.chat.id

            logging.info(
                f"🔗 Linking Telegram chat {chat_id} with user {user_id}")

            try:
                resp = requests.post(
                    f"{API_BASE}/telegram/register",
                    json={"user_id": user_id, "chat_id": str(chat_id)},
                    timeout=5
                )
                print(resp.text)
                if resp.ok:
                    await message.answer("✅ Your Telegram is now connected! You will receive daily appointment alerts.")
                else:
                    await message.answer("❌ Failed to connect your account. Please try again.")
            except Exception as e:
                logging.error(f"Failed to call backend: {e}")
                await message.answer("⚠️ Could not connect to the server. Please try again later.")
        else:
            await message.answer(
                "👋 Welcome to Bürgeramt Slot Finder!\n\n"
                "Please connect your account from the app using the 'Connect Telegram' button."
            )
