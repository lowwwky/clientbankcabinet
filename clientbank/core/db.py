from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("postgresql+psycopg://postgres:deaftonequeen2006%@@@localhost:5432/clientbank")
SessionLocal = sessionmaker(bind=engine, autoflush = False, expire_on_commit=False)

class Base(DeclarativeBase):
    ...

def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()