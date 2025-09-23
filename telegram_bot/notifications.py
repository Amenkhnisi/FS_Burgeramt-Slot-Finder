import logging
import requests
from datetime import datetime
import zoneinfo

berlin_tz = zoneinfo.ZoneInfo("Europe/Berlin")


def send_daily_notifications(bot, settings):
    async def job():
        now = datetime.now(berlin_tz).strftime("%H:%M")
        logging.info(f"⏰ Checking notifications for {now}")

        try:
            resp = requests.get(
                f"{settings.api_base}/{settings.api_version}/telegram/notify-due?time={now}", timeout=10)
            if not resp.ok:
                logging.warning("⚠️ Failed to fetch notify-due users")
                return

            users = resp.json()
            if not users:
                logging.info("ℹ️ No users to notify")
                return
            for u in users:
                chat_id = u["chat_id"]
                slots = u["slots"]

                if not slots:
                    text = "📭 Keine verfügbaren Bürgeramt-Termine heute."
                else:
                    text = "📅 Verfügbare Termine:\n\n"
                    for s in slots:
                        text += f"➡️ {s['date']} – {s['label']}\n🔗 {s['link']}\n\n"

                try:
                    await bot.send_message(chat_id, text)
                    logging.info(f"✅ Sent to {chat_id}")
                except Exception as e:
                    logging.error(f"❌ Failed to send to {chat_id}: {e}")
        except Exception as e:
            logging.error(f"❌ Notification error: {e}")
    return job
