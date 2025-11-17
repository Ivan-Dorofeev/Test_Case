from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.company import Company


class CRUDCompany:
    """CRUD для модели Company (только работа с БД, без бизнес-логики)."""

    # Словарь для проверки уникальности полей
    UNIQUE_FIELDS = {
        "INN": lambda db, val: db.query(Company).filter(Company.INN == val).first(),
        "OGRN": lambda db, val: db.query(Company).filter(Company.OGRN == val).first(),
    }

    def get(self, db: Session, company_id: int, include_deleted: bool = False) -> Optional[Company]:
        """Получить компанию по ID.
        - include_deleted=True позволяет вернуть удалённую компанию.
        """
        query = db.query(Company).filter(Company.id == company_id)
        if not include_deleted:
            query = query.filter(Company.deleted_at.is_(None))
        return query.first()

    def list(
        self,
        db: Session,
        founder_id: Optional[int] = None,
        include_deleted: bool = False,
        status: Optional[str] = None,
        type: Optional[int] = None,
        is_public: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> list[Company]:
        """Получить список компаний с фильтрацией и поиском.

        Фильтры:
        - founder_id: только компании конкретного пользователя
        - status: фильтр по статусу
        - type: фильтр по типу
        - is_public: фильтр по публичности
        - include_deleted: включить удалённые компании
        - search: поиск по INN, OGRN или имени компании
        """
        query = db.query(Company)

        # динамические фильтры через словарь
        filters = {"founder_id": founder_id, "status": status, "type": type, "is_public": is_public}
        for attr, value in filters.items():
            if value is not None:
                query = query.filter(getattr(Company, attr) == value)

        if not include_deleted:
            query = query.filter(Company.deleted_at.is_(None))

        if search:
            like = f"%{search}%"
            query = query.filter((Company.INN.ilike(like)) | (Company.OGRN.ilike(like)) | (Company.name.ilike(like)))

        return query.all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> Company:
        """Создать новую компанию.
        - obj_in: словарь с полями компании
        - выбрасывает ValueError, если INN или OGRN уже существуют
        """
        company = Company(**obj_in)
        db.add(company)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Компания с таким INN или OGRN уже существует") from None
        db.refresh(company)
        return company

    def update(self, db: Session, company: Company, update_data: Dict[str, Any]) -> Company:
        """Обновить существующую компанию.
        - update_data: словарь с обновляемыми полями
        """
        for k, v in update_data.items():
            setattr(company, k, v)
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    def set_deleted_state(self, db: Session, company: Company, deleted: bool) -> Company:
        """Soft-delete или восстановление компании.
        - deleted=True — пометить как удалённую
        - deleted=False — восстановить компанию
        """
        company.deleted_at = datetime.utcnow() if deleted else None
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    def hard_delete(self, db: Session, company: Company) -> None:
        """Полностью удалить компанию из базы данных.
        - Использовать только для hard delete (суперпользователь)
        """
        db.delete(company)
        db.commit()


# Экземпляр CRUD для использования в сервисах
company_crud = CRUDCompany()
