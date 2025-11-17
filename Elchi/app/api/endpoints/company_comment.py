"""API маршруты для работы с комментариями к компаниям и ответами компаний."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.company_comment import (
    CompanyCommentCreate,
    CompanyCommentRead,
    CompanyCommentUpdate,
    CompanyReplyCreate,
    CompanyReplyRead,
    CompanyReplyUpdate,
)
from app.services.company_comment_service import CompanyCommentService, CompanyReplyService

router = APIRouter()


# -------------------- COMMENTS --------------------


@router.post("/", response_model=CompanyCommentRead, summary="Создать комментарий к компании")
def create_comment(
    data: CompanyCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyCommentRead:
    """Создание комментария к компании."""
    return CompanyCommentRead.model_validate(CompanyCommentService.create_comment(db, data, current_user))


@router.get("/company/{company_id}", response_model=List[CompanyCommentRead], summary="Список комментариев компании")
def list_comments_by_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[CompanyCommentRead]:
    """Получение списка комментариев компании."""
    comments = CompanyCommentService.list_by_company(db, company_id, current_user)
    return [CompanyCommentRead.model_validate(c) for c in comments]


@router.get("/user/{user_id}", response_model=List[CompanyCommentRead], summary="Список комментариев пользователя")
def list_comments_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[CompanyCommentRead]:
    """Получение комментариев конкретного пользователя."""
    comments = CompanyCommentService.list_by_user(db, user_id, current_user)
    return [CompanyCommentRead.model_validate(c) for c in comments]


@router.get("/{comment_id}", response_model=CompanyCommentRead, summary="Получить комментарий по ID")
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyCommentRead:
    """Получение одного комментария по ID."""
    return CompanyCommentRead.model_validate(CompanyCommentService.get_comment(db, comment_id, current_user))


@router.patch("/{comment_id}", response_model=CompanyCommentRead, summary="Обновить комментарий")
def update_comment(
    comment_id: int,
    data: CompanyCommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyCommentRead:
    """Обновление комментария."""
    return CompanyCommentRead.model_validate(CompanyCommentService.update_comment(db, comment_id, data, current_user))


@router.delete("/{comment_id}", summary="Удалить комментарий")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """Удаление комментария."""
    return CompanyCommentService.delete_comment(db, comment_id, current_user)


# -------------------- REPLIES --------------------


@router.post("/reply", response_model=CompanyReplyRead, summary="Создать ответ компании на комментарий")
def create_reply(
    data: CompanyReplyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyReplyRead:
    """Создание ответа компании на комментарий."""
    return CompanyReplyRead.model_validate(CompanyReplyService.create_reply(db, data, current_user))


@router.get("/reply/{reply_id}", response_model=CompanyReplyRead, summary="Получить ответ по ID")
def get_reply(
    reply_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyReplyRead:
    """Получение одного ответа компании по ID."""
    return CompanyReplyRead.model_validate(CompanyReplyService.get_reply(db, reply_id, current_user))


@router.get("/reply/company/{company_id}", response_model=List[CompanyReplyRead], summary="Список ответов компании")
def list_replies_by_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[CompanyReplyRead]:
    """Получение всех ответов компании."""
    replies = CompanyReplyService.list_by_company(db, company_id, current_user)
    return [CompanyReplyRead.model_validate(r) for r in replies]


@router.patch("/reply/{reply_id}", response_model=CompanyReplyRead, summary="Обновить ответ компании")
def update_reply(
    reply_id: int,
    data: CompanyReplyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyReplyRead:
    """Обновление ответа компании."""
    return CompanyReplyRead.model_validate(CompanyReplyService.update_reply(db, reply_id, data, current_user))


@router.delete("/reply/{reply_id}", summary="Удалить ответ компании")
def delete_reply(
    reply_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    """Удаление ответа компании."""
    return CompanyReplyService.delete_reply(db, reply_id, current_user)
