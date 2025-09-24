from sqlalchemy.orm import Session
from app import models
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).get(user_id)


def create_user(db: Session, username: str, password: str, email: str = None):
    hashed = pwd_context.hash(password)
    user = models.User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


# Telegram-related CRUD operations

def get_telegram_user(db: Session, user_id: int) -> models.TelegramUser | None:
    return db.query(models.TelegramUser).filter(models.TelegramUser.user_id == user_id).first()


def create_telegram_user(db: Session, user_id: int, chat_id: str, notify_time: str) -> models.TelegramUser:
    tg_user = models.TelegramUser(
        user_id=user_id, chat_id=chat_id, notify_time=notify_time)
    db.add(tg_user)
    db.commit()
    db.refresh(tg_user)
    return tg_user


def update_notify_time(db: Session, user_id: int, new_time: str) -> models.TelegramUser | None:
    tg_user = get_telegram_user(db, user_id)
    if tg_user:
        tg_user.notify_time = new_time
        db.commit()
        db.refresh(tg_user)
    else:
        return {"error": "User not found"}
    return tg_user
