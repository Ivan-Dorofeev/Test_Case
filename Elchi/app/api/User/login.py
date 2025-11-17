from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud.user.user import user_crud
from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.user.login import (
    LoginStep1Request,
    LoginStep1Response,
    LoginStep2Request,
    LoginStep2Response,
    LoginStep3Request,
    TokenResponse,
)
from app.services.user.auth_service import AuthService

router = APIRouter()


@router.post("/login-email-step1", response_model=LoginStep1Response, summary="Проверка email (шаг 1)")
def login_step1(data: LoginStep1Request, db: Session = Depends(get_db)) -> LoginStep1Response:
    """Проверяет, существует ли пользователь с указанным email."""
    exists = user_crud.get_by_email(db, data.email)
    return LoginStep1Response(exists=exists is not None)


@router.post(
    "/login-email-step2", response_model=LoginStep2Response, summary="Авторизация по паролю и отправка кода (шаг 2)"
)
def login_step2(data: LoginStep2Request, db: Session = Depends(get_db)) -> LoginStep2Response:
    """Проверяет email и пароль, отправляет код подтверждения на почту."""
    result = AuthService.step2_send_code(db, data.email, data.password)
    return LoginStep2Response(**result)


@router.post("/login-email-step3", response_model=TokenResponse, summary="Подтверждение кода и выдача токена (шаг 3)")
def login_step3(data: LoginStep3Request, db: Session = Depends(get_db)) -> TokenResponse:
    """Валидирует код подтверждения и возвращает JWT-токен."""
    token_data = AuthService.step3_verify_code(db, data.email, data.code)
    return TokenResponse(**token_data)


@router.post("/login", response_model=TokenResponse, summary="Авторизация через OAuth2")
def login_oauth2(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """Авторизация по email и паролю (OAuth2 Password Flow)."""
    token_data = AuthService.oauth2_login(db, form_data.username, form_data.password)
    return TokenResponse(**token_data)


@router.post("/logout", summary="Выход из системы")
def logout(current_user: User = Depends(get_current_active_user)) -> dict[str, str]:
    """Завершает сессию. Клиенту нужно удалить токен."""
    return {"message": "Вы успешно вышли"}


@router.post("/refresh-token", response_model=TokenResponse, summary="Обновление токена")
def refresh_token(current_user: User = Depends(get_current_active_user)) -> TokenResponse:
    """Генерирует новый access_token для текущего пользователя."""
    token_data = AuthService.generate_token(current_user)
    return TokenResponse(**token_data)
