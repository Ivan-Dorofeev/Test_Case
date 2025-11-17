"""Модуль CRUD для работы с комментариями к компаниям и ответами на них.

Содержит два класса:
- CRUDCompanyComment: операции получения, создания, обновления и удаления комментариев.
- CRUDCompanyReply: операции получения, создания, обновления и удаления ответов компании на комментарии.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models.company_comment import CompanyComment, CompanyReply


class CRUDCompanyComment:
    """Класс для CRUD-операций с комментариями к компаниям."""

    def get(self, db: Session, comment_id: int) -> Optional[CompanyComment]:
        """Получить комментарий по ID, подгружая связанную компанию."""
        return (
            db.query(CompanyComment)
            .options(joinedload(CompanyComment.company))
            .filter(CompanyComment.id == comment_id)
            .first()
        )

    def list_by_company(self, db: Session, company_id: int) -> List[CompanyComment]:
        """Получить список всех комментариев для указанной компании."""
        return db.query(CompanyComment).filter(CompanyComment.company_id == company_id).all()

    def list_by_user(self, db: Session, user_id: int) -> List[CompanyComment]:
        """Получить список всех комментариев, оставленных указанным пользователем."""
        return db.query(CompanyComment).filter(CompanyComment.user_id == user_id).all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> CompanyComment:
        """Создать новый комментарий к компании."""
        comment = CompanyComment(**obj_in)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    def update(self, db: Session, comment: CompanyComment, update_data: Dict[str, Any]) -> CompanyComment:
        """Обновить поля существующего комментария."""
        for k, v in update_data.items():
            setattr(comment, k, v)
        db.commit()
        db.refresh(comment)
        return comment

    def delete(self, db: Session, comment: CompanyComment) -> None:
        """Удалить комментарий из базы данных."""
        db.delete(comment)
        db.commit()


class CRUDCompanyReply:
    """Класс для CRUD-операций с ответами компании на комментарии."""

    def get(self, db: Session, reply_id: int) -> Optional[CompanyReply]:
        """Получить ответ по ID."""
        return db.query(CompanyReply).filter(CompanyReply.id == reply_id).first()

    def list_by_company(self, db: Session, company_id: int) -> List[CompanyReply]:
        """Получить список всех ответов компании."""
        return db.query(CompanyReply).filter(CompanyReply.company_id == company_id).all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> CompanyReply:
        """Создать новый ответ компании на комментарий."""
        reply = CompanyReply(**obj_in)
        db.add(reply)
        db.commit()
        db.refresh(reply)
        return reply

    def update(self, db: Session, reply: CompanyReply, update_data: Dict[str, Any]) -> CompanyReply:
        """Обновить поля существующего ответа."""
        for k, v in update_data.items():
            setattr(reply, k, v)
        db.commit()
        db.refresh(reply)
        return reply

    def delete(self, db: Session, reply: CompanyReply) -> None:
        """Удалить ответ компании из базы данных."""
        db.delete(reply)
        db.commit()


# Экземпляры классов для использования в сервисном слое
company_comment_crud = CRUDCompanyComment()
company_reply_crud = CRUDCompanyReply()
