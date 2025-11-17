from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.notifications import Notification
from app.models.user import User
from app.schemas.notifications import (
    NotificationCreate,
    NotificationReadShort,
    NotificationUpdate,
)
from app.services.notification_service import NotificationService

router = APIRouter()


@router.post("/", response_model=NotificationReadShort, summary="Создать уведомление")
def create_notification(
    data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Notification:
    """Создаёт новое уведомление. Доступно только суперпользователям."""
    return NotificationService.create_notification(db, data, current_user)


@router.get(
    "/user",
    response_model=List[NotificationReadShort],
    summary="Список уведомлений текущего пользователя",
)
def list_user_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[Notification]:
    """Возвращает все уведомления, принадлежащие текущему пользователю."""
    return NotificationService.list_user_notifications(db, current_user)


@router.get(
    "/{notification_id}",
    response_model=NotificationReadShort,
    summary="Получить уведомление по ID",
)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Notification:
    """Получить одно уведомление по его ID. Доступно только владельцу уведомления или суперпользователю."""
    return NotificationService.get_notification(db, notification_id, current_user)


@router.patch(
    "/{notification_id}",
    response_model=NotificationReadShort,
    summary="Обновить уведомление",
)
def update_notification(
    notification_id: int,
    data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Notification:
    """Обновить уведомление (например, изменить текст)."""
    return NotificationService.update_notification(db, notification_id, data, current_user)


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationReadShort,
    summary="Пометить уведомление как прочитанное",
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Notification:
    """Отметить уведомление как прочитанное."""
    return NotificationService.mark_as_read(db, notification_id, current_user)


@router.delete(
    "/{notification_id}",
    response_model=Dict[str, str],
    summary="Удалить уведомление",
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, str]:
    """Удалить уведомление. Доступно только владельцу уведомления или суперпользователю."""
    return NotificationService.delete_notification(db, notification_id, current_user)
