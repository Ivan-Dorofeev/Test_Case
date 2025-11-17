from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):  # type: ignore[misc]
    """Базовый класс для всех моделей."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Генератор SQLAlchemy Session для Depends."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
