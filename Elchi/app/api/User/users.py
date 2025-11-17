"""Роутер для работы с пользователями.

Поддерживает:
- Получение профиля текущего пользователя
- Получение списка пользователей (с фильтрацией и поиском)
- Получение одного пользователя
- Обновление пользователя
- Включение/выключение активности
- Удаление (soft/hard)
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud.user.user import user_crud
from app.database.database import get_db
from app.dependencies.auth import get_current_active_superuser, get_current_active_user
from app.models.enums.Enum_Model import CompanyUserRole
from app.models.user import User
from app.schemas.user.user import UserReadFull, UserReadWithId, UserUpdate
from app.services.user.user_service import UserService
from app.utils.http import not_found

router = APIRouter()


# -------------------- PROFILE --------------------
@router.get("/me", response_model=UserReadFull, summary="Профиль текущего пользователя")
def read_own_profile(current_user: User = Depends(get_current_active_user)) -> User:
    """Получение профиля текущего пользователя.
    Доступно только авторизованному пользователю.
    """
    return current_user


@router.patch("/me", response_model=UserReadFull, summary="Обновить профиль текущего пользователя")
def update_own_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> UserReadFull:
    """Обновление профиля текущего пользователя.

    - Пользователь может изменить только разрешённые поля.
    - Нельзя менять email, роль или права суперюзера.
    """
    current_user_db = user_crud.get(db, current_user.id)
    if not current_user_db:
        raise not_found("Пользователь не найден")

    updated_user = user_crud.update(db, current_user_db, user_update.model_dump(exclude_unset=True))
    return updated_user


# -------------------- USERS --------------------
@router.get("/", response_model=List[UserReadWithId], summary="Список пользователей с фильтрацией и поиском")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
    include_deleted: bool = Query(False, description="Показывать удалённых пользователей"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    is_superuser: Optional[bool] = Query(None, description="Фильтр по суперюзеру"),
    role: Optional[CompanyUserRole] = Query(None, description="Фильтр по роли пользователя"),
    search: Optional[str] = Query(None, description="Поиск по email или телефону"),
) -> List[User]:
    """Получение списка пользователей с возможностью фильтрации и поиска.

    Доступно только суперюзеру.
    """
    return user_crud.list(
        db=db,
        include_deleted=include_deleted,
        is_active=is_active,
        is_superuser=is_superuser,
        role=role,
        search=search,
    )


@router.get("/{user_id}", response_model=UserReadFull, summary="Получить пользователя по ID")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> User:
    """Получение информации о конкретном пользователе по ID.
    Доступно только суперюзеру.
    """
    user = user_crud.get(db, user_id)
    if not user:
        raise not_found("Пользователь не найден")
    return user


@router.patch("/{user_id}", response_model=UserReadFull, summary="Обновить пользователя")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Обновление данных пользователя.

    - Обычные пользователи могут менять только свои данные.
    - Суперпользователь может менять любые данные.
    - Нельзя обновлять удалённых пользователей.
    """
    return UserService.update_user(db, user_id, data, acting_user=current_user)


@router.post("/{user_id}/toggle-active", summary="Включить/выключить активность пользователя")
def toggle_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> dict[str, object]:
    """Переключение статуса активности пользователя.
    Доступно только суперюзеру.
    """
    return UserService.toggle_user_active(db, user_id, current_user)


@router.delete("/{user_id}", summary="Удалить пользователя (soft/hard)")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    hard: bool = Query(False, description="Если True — удаление безвозвратно"),
) -> dict[str, str]:
    """Удаление пользователя.

    - Soft delete: можно удалить себя или другой аккаунт (если суперюзер)
    - Hard delete: только для суперюзера
    """
    UserService.delete_user(db, user_id, current_user, hard)
    return {"message": "Пользователь удалён"}
