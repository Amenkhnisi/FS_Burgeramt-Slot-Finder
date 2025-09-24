from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    username: str
    password: str


# Telegram-related schemas

class TelegramUserBase(BaseModel):
    notify_time: str


class TelegramUserCreate(TelegramUserBase):
    user_id: int
    chat_id: str


class TelegramUserOut(TelegramUserBase):
    chat_id: str

    model_config = ConfigDict(from_attributes=True)
