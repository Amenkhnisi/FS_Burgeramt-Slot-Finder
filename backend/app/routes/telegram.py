from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas,  models
from app.utils.auth_utils import get_current_user, verify_api_key
import os
import datetime as datetime
import zoneinfo
from app.services.scraper import scrape_appointments_playwright_sync


router = APIRouter(prefix="/telegram", tags=["Telegram"])

# Register user for notifier

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
berlin_tz = zoneinfo.ZoneInfo("Europe/Berlin")


# Update notify time


@router.put("/time")
def update_notify_time(payload: schemas.TelegramUserBase, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_notify_time(db, user.id, payload.notify_time)

# Get current user's Telegram info


@router.get("/me")
def get_my_telegram(user=Depends(get_current_user), db: Session = Depends(get_db),   # Enforce API key check
                    ):
    tg = crud.get_telegram_user(db, user.id)
    if not tg:
        raise HTTPException(404, "Not registered in Telegram notifier")
    return tg

# Get all users (used by bot scheduler)


TELEGRAM_BOT_NAME = os.environ.get(
    "TELEGRAM_BOT_NAME", "BerlinAppointmentapiBot")

# For debugging - get all registered users


@router.get("/all-users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.TelegramUser).all()
    return [{"chat_id": u.chat_id, "notify_time": u.notify_time} for u in users]

# Generate Telegram deep link for user to connect bot


@router.post("/connect")
def connect_telegram(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Generate a Telegram deep link for the authenticated user.
    The bot will handle /start uid_{userId} and register chat_id.
    """
    deep_link = f"https://t.me/{TELEGRAM_BOT_NAME}?start=uid_{user.id}"
    return {"deep_link": deep_link}

# Register user (called from bot when user clicks deep link)


@router.post("/register")
def register_telegram(payload: dict, db: Session = Depends(get_db)):
    """
    Called from telegram_bot.py when user clicks deep link (/start uid_x).
    """
    user_id = payload.get("user_id")
    chat_id = payload.get("chat_id")
    if not user_id or not chat_id:
        raise HTTPException(400, "Missing user_id or chat_id")

    tg_user = crud.get_telegram_user(db, user_id)
    if tg_user:
        tg_user.chat_id = chat_id  # update chat_id if changed
        db.commit()
        return {"msg": "Already registered", "chat_id": chat_id}

    tg_user = crud.create_telegram_user(
        db, user_id, chat_id, notify_time=datetime.datetime.now(berlin_tz).strftime("%H:%M"))
    return {"msg": "Registered successfully", "chat_id": tg_user.chat_id, "notify_time": tg_user.notify_time}


# Endpoint to get users due for notification (used by bot scheduler)


@router.get("/notify-due")
def notify_due(time: str | None = None, db: Session = Depends(get_db), _: None = Depends(verify_api_key)):
    """
    Return all users whose notify_time matches the current Berlin time (HH:MM).
    If ?time=HH:MM is passed, it overrides (for debugging/testing).
    """
    if time is None:
        time = datetime.datetime.now(berlin_tz).strftime("%H:%M")

    users = db.query(models.TelegramUser).filter(
        models.TelegramUser.notify_time == time
    ).all()

    # For each user, fetch today's slots from scraper

    slots = scrape_appointments_playwright_sync()

    results = []
    for u in users:
        # Fetch today's slots from wherever you store them
        results.append({
            "chat_id": u.chat_id,
            "slots": slots
        })

    return results
