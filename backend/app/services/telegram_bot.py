import os
import requests
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(chat_id: str, text: str):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})


def get_updates(offset=None):
    url = f"{TELEGRAM_API_URL}/getUpdates"
    params = {"timeout": 60}
    if offset:
        params["offset"] = offset
    resp = requests.get(url, params=params).json()
    return resp.get("result", [])


def process_updates():
    db: Session = SessionLocal()
    updates = get_updates()

    for update in updates:
        message = update.get("message")
        if not message:
            continue

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # Look for deep link: /start uid_123
        if text.startswith("/start"):
            parts = text.split()
            if len(parts) > 1 and parts[1].startswith("uid_"):
                user_id = parts[1].replace("uid_", "")

                user = db.query(User).filter(User.id == int(user_id)).first()
                if user:
                    user.telegram_chat_id = str(chat_id)
                    db.commit()
                    send_message(
                        chat_id, "✅ Connected! You'll now receive daily appointment notifications.")
                else:
                    send_message(chat_id, "⚠️ Invalid link, please try again.")

    db.close()
