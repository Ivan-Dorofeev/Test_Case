from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.User.email_confirmation import EmailConfirmation

MAX_FAILED_ATTEMPTS = 5


class CRUDConfirmation:
    """CRUD для работы с EmailConfirmation."""

    def create(self, db: Session, user_id: int, code: str, purpose: str, expires_at: datetime) -> EmailConfirmation:
        """Создаёт запись кода в БД."""
        db_obj = EmailConfirmation(user_id=user_id, code=code, purpose=purpose, expires_at=expires_at, attempts=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_last(self, db: Session, user_id: int, purpose: str) -> Optional[EmailConfirmation]:
        """Возвращает последний код для пользователя по цели."""
        return (
            db.query(EmailConfirmation)
            .filter(EmailConfirmation.user_id == user_id, EmailConfirmation.purpose == purpose)
            .order_by(EmailConfirmation.created_at.desc())
            .first()
        )

    def delete_all(self, db: Session, user_id: int, purpose: str) -> None:
        """Удаляет все коды по цели."""
        db.query(EmailConfirmation).filter(
            EmailConfirmation.user_id == user_id, EmailConfirmation.purpose == purpose
        ).delete()
        db.commit()

    def increment_attempts(self, db: Session, confirm: EmailConfirmation) -> None:
        """Увеличивает число попыток."""
        confirm.attempts += 1
        db.commit()
        db.refresh(confirm)


confirmation_crud = CRUDConfirmation()
