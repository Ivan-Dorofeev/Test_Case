"""Модуль password_routes.

Маршруты для управления паролями:
- запрос и проверка кода сброса;
- подтверждение сброса пароля;
- изменение пароля активным пользователем.
"""

from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_active_user
from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.user.password import (
    ChangePasswordRequest,
    PasswordResetConfirmRequest,
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordResetVerify,
    PasswordResetVerifyResponse,
)
from app.services.user.password_service import password_service

router = APIRouter()


@router.post("/password-reset/request", response_model=PasswordResetResponse, summary="Запрос сброса пароля")
def password_reset_request(
    data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> PasswordResetResponse:
    """Отправляет код сброса пароля на email пользователя."""
    result: dict[str, Any] = password_service.request_reset(db, data.email, background_tasks)
    return PasswordResetResponse(**result)


@router.post("/password-reset/verify", response_model=PasswordResetVerifyResponse, summary="Проверка кода сброса")
def password_reset_verify(
    data: PasswordResetVerify,
    db: Session = Depends(get_db),
) -> PasswordResetVerifyResponse:
    """Проверяет код сброса пароля из письма."""
    password_service.verify_code(db, data.email, data.code)
    return PasswordResetVerifyResponse(message="Код подтвержден, можно задать новый пароль")


@router.post("/password-reset/confirm", response_model=PasswordResetResponse, summary="Подтверждение сброса пароля")
def password_reset_confirm(
    data: PasswordResetConfirmRequest,
    db: Session = Depends(get_db),
) -> PasswordResetResponse:
    """Устанавливает новый пароль после проверки кода."""
    result = password_service.confirm_reset(db, data.email, data.code, data.password)
    return PasswordResetResponse(**result)


@router.post("/change-password", response_model=PasswordResetResponse, summary="Изменение пароля")
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PasswordResetResponse:
    """Изменяет пароль активного пользователя после проверки старого."""
    result = password_service.change_password(db, current_user, data.old_password, data.password)
    return PasswordResetResponse(**result)
