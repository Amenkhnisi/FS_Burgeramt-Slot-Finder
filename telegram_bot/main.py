import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Settings
from handlers.start import register_start_handler
from scheduler import setup_scheduler

# ==============================
# Initialization
# ==============================

settings = Settings()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# ==============================
# Entrypoint
# ==============================


async def main():
    register_start_handler(dp)
    setup_scheduler(scheduler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
