"""Зависимости (dependencies) для FastAPI.

Модуль содержит функции-зависимости, которые можно использовать
в эндпоинтах: получение сессии БД, текущего пользователя и т.д.
"""

from typing import Generator

from sqlalchemy.orm import Session

from app.database.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Зависимость для получения сессии базы данных.

    Используется в эндпоинтах через Depends(get_db).
    Автоматически открывает и закрывает сессию.

    Yields:
        Session: Сессия SQLAlchemy.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
