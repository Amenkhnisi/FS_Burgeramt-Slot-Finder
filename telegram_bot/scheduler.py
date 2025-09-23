from notifications import send_daily_notifications
from aiogram import Bot
from config import Settings

settings = Settings()

bot = Bot(token=settings.telegram_bot_token)


def setup_scheduler(scheduler):
    # Run every minute
    scheduler.add_job(send_daily_notifications(
        bot, settings), "cron", minute="*")
    scheduler.start()
