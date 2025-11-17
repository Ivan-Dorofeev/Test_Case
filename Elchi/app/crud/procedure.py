# app/crud/procedure.py
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from app.models.procedure import Procedure
from app.schemas.procedure import ProcedureCreate, ProcedureUpdate


class CRUDProcedure:
    """CRUD-операции для модели Procedure."""

    def get(self, db: Session, id: int) -> Optional[Procedure]:
        """Получить процедуру по ID."""
        return db.query(Procedure).filter(Procedure.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Procedure]:
        """Получить список процедур с пагинацией."""
        return db.query(Procedure).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ProcedureCreate) -> Procedure:
        """Создать новую процедуру."""
        procedure_data = obj_in.model_dump()
        db_obj = Procedure(**procedure_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: Procedure,
        obj_in: ProcedureUpdate,
    ) -> Procedure:
        """Обновить существующую процедуру."""
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[Procedure]:
        """Удалить процедуру по ID."""
        obj = db.query(Procedure).filter(Procedure.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


procedure_crud = CRUDProcedure()