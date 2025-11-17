from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.announcement import announcement
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.announcement import AnnouncementCreate, AnnouncementReadFull, AnnouncementReadShort, AnnouncementUpdate

router = APIRouter()


@router.post(
    "/", response_model=AnnouncementReadShort, status_code=status.HTTP_201_CREATED, summary="Создать объявление"
)
def create_announcement(
    announcement_data: AnnouncementCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> AnnouncementReadShort:
    """Создать новое объявление."""
    if announcement_data.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Нельзя создавать объявления от имени другого пользователя"
        )
    return announcement.create(db, announcement_data)


@router.get("/my/{announcement_id}", response_model=AnnouncementReadFull, summary="Просмотр своего объявления")
def get_my_announcement(
    announcement_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> AnnouncementReadFull:
    """Получить своё объявление по ID."""
    db_announcement = announcement.get(db, announcement_id)

    if not db_announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объявление не найдено")

    if db_announcement.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к чужому объявлению")

    return db_announcement


@router.get("/my", response_model=List[AnnouncementReadShort], summary="Просмотр всех своих объявлений")
def get_my_announcements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[AnnouncementReadShort]:
    """Получить все объявления текущего пользователя."""
    return announcement.get_user_announcements(db, current_user.id, skip, limit)


@router.get("/{announcement_id}", response_model=AnnouncementReadFull, summary="Просмотр любого объявления")
def get_announcement(announcement_id: int, db: Session = Depends(get_db)) -> AnnouncementReadFull:
    """Получить объявление по ID."""
    db_announcement = announcement.get(db, announcement_id)

    if not db_announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объявление не найдено")

    return db_announcement


@router.get("/", response_model=List[AnnouncementReadShort], summary="Просмотр всех объявлений")
def get_announcements(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)
) -> List[AnnouncementReadShort]:
    """Получить все объявления."""
    return announcement.get_multi(db, skip, limit)


@router.put("/my/{announcement_id}", response_model=AnnouncementReadShort, summary="Редактирование своего объявления")
def update_my_announcement(
    announcement_id: int,
    announcement_data: AnnouncementUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AnnouncementReadShort:
    """Обновить своё объявление."""
    db_announcement = announcement.get(db, announcement_id)

    if not db_announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объявление не найдено")
    if db_announcement.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на редактирование этого объявления")
    return announcement.update(db, db_announcement, announcement_data)
