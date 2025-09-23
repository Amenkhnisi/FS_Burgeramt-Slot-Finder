from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

# FastAPI dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
