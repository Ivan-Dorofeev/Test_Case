"""Зависимости для аутентификации и авторизации пользователей.
Использует OAuth2 Bearer токены и проверяет активность/роль пользователя.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_token
from app.crud.user.user import user_crud
from app.database.database import get_db
from app.models.user import User

# OAuth2 схема для извлечения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Получает пользователя по JWT токену.

    Raises:
        HTTPException 401: если токен недействителен или пользователь не найден.

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(token)
        user_id_any = payload.get("sub")
        if not isinstance(user_id_any, str):
            raise credentials_exception
        user_id: str = user_id_any
    except JWTError:
        raise credentials_exception from None

    db_user = user_crud.get(db, user_id=int(user_id))
    if db_user is None:
        raise credentials_exception
    return db_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Проверяет, что пользователь активен."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    """Проверяет, что пользователь является суперюзером."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
    return current_user
