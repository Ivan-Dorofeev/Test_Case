from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user.register import (
    ConfirmEmailRequest,
    RegisterRequest,
    ResendConfirmationRequest,
)
from app.services.user.user_service import UserService

router = APIRouter()


@router.post("/register", status_code=201, summary="Регистрация пользователя")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Создает пользователя и отправляет код подтверждения на email."""
    UserService.register_user(db, data)
    return {"message": "Пользователь зарегистрирован. Код подтверждения отправлен на email."}


@router.post("/confirm", summary="Подтверждение email")
def confirm_email(data: ConfirmEmailRequest, db: Session = Depends(get_db)) -> Any:
    """Подтверждает email с помощью кода."""
    return UserService.confirm_email(db, data.email, data.code)


@router.post("/resend-confirmation", summary="Повторная отправка кода")
def resend_confirmation(data: ResendConfirmationRequest, db: Session = Depends(get_db)) -> Any:
    """Отправляет новый код подтверждения email."""
    return UserService.resend_confirmation(db, data.email)
