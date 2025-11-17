from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.models.signature import DigitalSignature


class CRUDSignature:
    """CRUD-операции для DigitalSignature."""

    @staticmethod
    def create(db: Session, **kwargs: Any) -> DigitalSignature:
        signature = DigitalSignature(**kwargs)
        db.add(signature)
        db.commit()
        db.refresh(signature)
        return signature

    @staticmethod
    def get(db: Session, signature_id: int) -> Optional[DigitalSignature]:
        return db.query(DigitalSignature).filter(DigitalSignature.id == signature_id).first()

    @staticmethod
    def list(db: Session, user_id: Optional[int] = None) -> List[DigitalSignature]:
        query = db.query(DigitalSignature)
        if user_id:
            query = query.filter(DigitalSignature.user_id == user_id)
        return query.all()

    @staticmethod
    def delete(db: Session, signature_id: int) -> bool:
        signature = CRUDSignature.get(db, signature_id)
        if not signature:
            return False
        db.delete(signature)
        db.commit()
        return True


crud_signature = CRUDSignature()
