from typing import Any, Dict, List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.enums.Enum_Model import CompanyUserRole
from app.models.user import User


class CRUDUser:
    """CRUD для модели User."""

    def get(self, db: Session, user_id: int, include_deleted: bool = False) -> Optional[User]:
        """Получить пользователя по ID."""
        query = db.query(User).filter(User.id == user_id)
        if not include_deleted:
            query = query.filter(User.deleted_at.is_(None))
        return query.first()

    def get_by_email(self, db: Session, email: str, include_deleted: bool = False) -> Optional[User]:
        """Получить пользователя по email."""
        query = db.query(User).filter(User.email == email)
        if not include_deleted:
            query = query.filter(User.deleted_at.is_(None))
        return query.first()

    def list(
        self,
        db: Session,
        include_deleted: bool = False,
        is_active: Optional[bool] = None,
        is_superuser: Optional[bool] = None,
        role: Optional[CompanyUserRole] = None,
        search: Optional[str] = None,
    ) -> List[User]:
        """Получить список пользователей с фильтрацией и поиском.

        Фильтры:
        - is_active: активные/неактивные пользователи
        - is_superuser: фильтр по роли суперюзера
        - role: роль пользователя
        - include_deleted: включить удалённых пользователей
        - search: поиск по email или телефону
        """
        query = db.query(User)

        # динамические фильтры через словарь
        filters = {"is_active": is_active, "is_superuser": is_superuser, "role": role}
        for attr, value in filters.items():
            if value is not None:
                query = query.filter(getattr(User, attr) == value)

        if not include_deleted:
            query = query.filter(User.deleted_at.is_(None))

        if search:
            like = f"%{search}%"
            query = query.filter((User.email.ilike(like)) | (User.phone.ilike(like)))

        return query.all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> User:
        """Создать нового пользователя."""
        user = User(**obj_in)
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(user)
        return user

    def update(self, db: Session, db_obj: User, update_data: Dict[str, Any]) -> User:
        """Обновить данные пользователя. Если указан пароль — хэширует его."""
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for k, v in update_data.items():
            setattr(db_obj, k, v)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_password(self, db: Session, user: User, new_password: str) -> User:
        """Обновить пароль пользователя (с хэшированием)."""
        user.hashed_password = get_password_hash(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def verify_password(self, plain: str, user: User) -> bool:
        """Проверить пароль пользователя."""
        return verify_password(plain, user.hashed_password)

    def soft_delete(self, db: Session, db_obj: User) -> User:
        """Пометить пользователя как удалённого (soft delete)."""
        db_obj.soft_delete()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def hard_delete(self, db: Session, db_obj: User) -> None:
        """Удалить пользователя полностью (hard delete)."""
        db.delete(db_obj)
        db.commit()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        """Авторизовать пользователя по email и паролю."""
        user = self.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = CRUDUser()
