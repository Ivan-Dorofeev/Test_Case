"""API-роуты для управления участниками компании: добавление, приглашение, принятие/отклонение и удаление."""

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models import CompanyUsers
from app.models.user import User
from app.schemas.company_users import CompanyUsersCreate, CompanyUsersReadShort
from app.services.company_users_service import CompanyUsersService

router = APIRouter()


@router.post("/add", response_model=CompanyUsersReadShort, summary="Добавить пользователя в компанию")
def add_user(
    data: CompanyUsersCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyUsers:
    """Добавление пользователя в компанию напрямую с ролью (не OWNER) и статусом ACTIVE."""
    return CompanyUsersService.add_user(db, data, current_user)


@router.post("/invite", response_model=CompanyUsersReadShort, summary="Пригласить пользователя в компанию")
def invite_user(
    data: CompanyUsersCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyUsers:
    """Создаёт приглашение пользователя в компанию с ролью (не OWNER) и статусом MODERATION."""
    return CompanyUsersService.invite_user(db, data, current_user, background_tasks)


@router.post("/{company_id}/accept", response_model=CompanyUsersReadShort, summary="Принять приглашение в компанию")
def accept_invite(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyUsers:
    """Пользователь принимает приглашение в компанию (статус MODERATION → ACTIVE)."""
    return CompanyUsersService.accept_invite(db, company_id, current_user)


@router.post("/{company_id}/decline", summary="Отклонить приглашение в компанию")
def decline_invite(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """Пользователь отклоняет приглашение в компанию (запись удаляется из БД)."""
    return CompanyUsersService.decline_invite(db, company_id, current_user)


@router.delete("/{company_id}/remove/{user_id}", summary="Удалить пользователя из компании")
def remove_user(
    company_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """Удаление пользователя из компании (нельзя удалить владельца)."""
    return CompanyUsersService.remove_user(db, company_id, user_id, current_user)
