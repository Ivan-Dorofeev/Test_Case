# app/api/endpoints/procedure_comment.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User # Импортируем модель User
from app.schemas import procedure_comment as pc_schema # Импортируем схемы
from app.services import procedure_comment_service as pc_service # Импортируем сервис

router = APIRouter()


@router.post("/", response_model=pc_schema.ProcedureCommentRead, summary="Создать комментарий к тендеру")
def create_procedure_comment(
    comment_in: pc_schema.ProcedureCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> pc_schema.ProcedureCommentRead:
    """
    Добавляет новый комментарий к указанной процедуре от текущего пользователя.
    """
    # Сервисный слой создаст комментарий, добавив user_id
    db_comment = pc_service.ProcedureCommentService.create_comment(db, data=comment_in, current_user=current_user)
    return db_comment


@router.get("/procedure/{procedure_id}", response_model=List[pc_schema.ProcedureCommentRead], summary="Получить комментарии к тендеру")
def get_comments_by_procedure(
    procedure_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> List[pc_schema.ProcedureCommentRead]:
    """
    Получает список комментариев для указанной процедуры.
    """
    comments = pc_service.ProcedureCommentService.get_comments_by_procedure(
        db, procedure_id=procedure_id, current_user=current_user, skip=skip, limit=limit
    )
    return comments


@router.get("/user/{user_id}", response_model=List[pc_schema.ProcedureCommentRead], summary="Получить комментарии пользователя")
def get_comments_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> List[pc_schema.ProcedureCommentRead]:
    """
    Получает список комментариев, оставленных указанным пользователем.
    """
    comments = pc_service.ProcedureCommentService.get_comments_by_user(
        db, user_id=user_id, current_user=current_user, skip=skip, limit=limit
    )
    return comments


@router.get("/{comment_id}", response_model=pc_schema.ProcedureCommentRead, summary="Получить комментарий по ID")
def get_procedure_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> pc_schema.ProcedureCommentRead:
    """
    Получает один комментарий по его ID.
    """
    comment = pc_service.ProcedureCommentService.get_comment(db, comment_id=comment_id, current_user=current_user)
    return comment


@router.patch("/{comment_id}", response_model=pc_schema.ProcedureCommentRead, summary="Обновить комментарий")
def update_procedure_comment(
    comment_id: int,
    comment_update: pc_schema.ProcedureCommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> pc_schema.ProcedureCommentRead:
    """
    Обновляет комментарий. Только автор комментария может его обновить.
    """
    updated_comment = pc_service.ProcedureCommentService.update_comment(
        db, comment_id=comment_id, data=comment_update, current_user=current_user
    )
    return updated_comment


@router.delete("/{comment_id}", summary="Удалить комментарий")
def delete_procedure_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> dict[str, str]:
    """
    Удаляет комментарий. Только автор комментария или суперюзер может его удалить.
    """
    result = pc_service.ProcedureCommentService.delete_comment(db, comment_id=comment_id, current_user=current_user)
    return result
