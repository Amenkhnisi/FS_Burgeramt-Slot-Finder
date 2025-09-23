from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=True)
    hashed_password = Column(String(256), nullable=False)
    telegram = relationship(
        "TelegramUser", back_populates="user", uselist=False)


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    chat_id = Column(String, unique=True, index=True)
    notify_time = Column(String, default="09:00")  # HH:MM format
    user = relationship("User", back_populates="telegram")

    def slots_to_send(self):
        """
        Placeholder: replace with real slot fetching logic
        """
        return ["Slot 1", "Slot 2", "Slot 3"]
