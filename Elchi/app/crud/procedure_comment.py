# app/crud/procedure_comment.py
from typing import Dict, List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.procedure_comment import ProcedureComment


class CRUDProcedureComment:
    """CRUD-операции для модели ProcedureComment."""

    def get(self, db: Session, id: int) -> Optional[ProcedureComment]:
        """Получить комментарий по ID."""
        return (
            db.query(ProcedureComment)
            .options(joinedload(ProcedureComment.user))
            .options(joinedload(ProcedureComment.procedure))
            .filter(ProcedureComment.id == id)
            .first()
        )

    def get_multi_by_procedure(
        self, db: Session, procedure_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[ProcedureComment]:
        """Получить список комментариев для указанной процедуры."""
        return (
            db.query(ProcedureComment)
            .filter(ProcedureComment.procedure_id == procedure_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_user(
        self, db: Session, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> List[ProcedureComment]:
        """Получить список комментариев, оставленных указанным пользователем."""
        return (
            db.query(ProcedureComment)
            .filter(ProcedureComment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, obj_in: Dict) -> ProcedureComment:
        """Создать новый комментарий."""
        db_obj = ProcedureComment(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ProcedureComment,
        obj_in: Dict,
    ) -> ProcedureComment:
        """Обновить комментарий."""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[ProcedureComment]:
        """Удалить комментарий по ID."""
        obj = db.query(ProcedureComment).filter(ProcedureComment.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


procedure_comment_crud = CRUDProcedureComment()