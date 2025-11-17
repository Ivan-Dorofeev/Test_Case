"""CRUD операции для объявлений."""

from typing import Any, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate


class CRUDAnnouncement:
    def get(self, db: Session, id: int) -> Optional[Announcement]:
        """Получить объявление по ID."""
        return db.query(Announcement).filter(Announcement.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """Получить список объявлений."""
        return db.query(Announcement).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: AnnouncementCreate) -> Announcement:
        """Создать новое объявление."""
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data.pop("files", None)
        obj_in_data.pop("works", None)
        obj_in_data.pop("comments", None)
        obj_in_data.pop("responses", None)

        db_obj = Announcement(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: Announcement, obj_in: Union[AnnouncementUpdate, Dict[str, Any]]
    ) -> Announcement:
        """Обновить существующее объявление."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[Announcement]:
        """Удалить объявление по ID."""
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_user_announcements(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Announcement]:
        """Получить все объявления пользователя."""
        return db.query(Announcement).filter(Announcement.creator_id == user_id).offset(skip).limit(limit).all()

    def get_with_relations(self, db: Session, id: int) -> Optional[Announcement]:
        """Получить объявление со всеми связанными объектами."""
        return db.query(Announcement).filter(Announcement.id == id).first()


announcement = CRUDAnnouncement()
