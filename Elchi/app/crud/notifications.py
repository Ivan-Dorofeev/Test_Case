from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.models.notifications import Notification


class CRUDNotification:
    """CRUD-операции для модели уведомлений."""

    def get(self, db: Session, notification_id: int) -> Optional[Notification]:
        """Получить уведомление по ID.
        Возвращает объект Notification или None, если не найдено.
        """
        return db.query(Notification).filter(Notification.id == notification_id).first()

    def list_by_user(self, db: Session, user_id: int) -> List[Notification]:
        """Вернуть все уведомления пользователя.
        Список может быть пустым, если уведомлений нет.
        """
        return db.query(Notification).filter(Notification.user_id == user_id).all()

    def create(self, db: Session, obj_in: dict[str, Any]) -> Notification:
        """Создать новое уведомление.
        Принимает словарь полей и возвращает сохранённый объект.
        """
        obj = Notification(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def mark_as_read(self, db: Session, notification_id: int) -> Optional[Notification]:
        """Отметить уведомление как прочитанное.
        Возвращает обновлённый объект или None, если уведомление не найдено.
        """
        notif = self.get(db, notification_id)
        if notif:
            notif.read = True
            db.commit()
            db.refresh(notif)
        return notif

    def update(self, db: Session, obj: Notification, update_data: dict[str, Any]) -> Notification:
        """Обновить поля уведомления.
        Принимает объект Notification и словарь изменяемых полей.
        """
        for k, v in update_data.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: Notification) -> None:
        """Удалить уведомление из базы.
        Принимает объект Notification и удаляет его без возврата значения.
        """
        db.delete(obj)
        db.commit()


notifications_crud = CRUDNotification()
