"""CRUD-операции для управления участниками компаний (CompanyUsers).
Позволяет получать, создавать, обновлять и удалять записи участников компании.
"""

from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.models.company_users import CompanyUsers


class CRUDCompanyUsers:
    """CRUD-класс для модели CompanyUsers."""

    def get(self, db: Session, company_id: int, user_id: int) -> Optional[CompanyUsers]:
        """Получить участника компании по company_id и user_id.
        Возвращает объект CompanyUsers или None, если не найден.
        """
        return (
            db.query(CompanyUsers)
            .filter(CompanyUsers.company_id == company_id, CompanyUsers.user_id == user_id)
            .first()
        )

    def list_by_company(self, db: Session, company_id: int) -> List[CompanyUsers]:
        """Получить список всех участников конкретной компании по company_id."""
        return db.query(CompanyUsers).filter(CompanyUsers.company_id == company_id).all()

    def create(self, db: Session, obj_in: dict[str, Any]) -> CompanyUsers:
        """Создать нового участника компании на основе переданных данных в виде словаря."""
        obj = CompanyUsers(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: CompanyUsers, update_data: dict[str, Any]) -> CompanyUsers:
        """Обновить существующего участника компании.
        update_data — словарь с полями для обновления.
        """
        for k, v in update_data.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: CompanyUsers) -> None:
        """Удалить участника компании из базы данных."""
        db.delete(obj)
        db.commit()


company_users_crud = CRUDCompanyUsers()
