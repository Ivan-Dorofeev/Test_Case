"""Тип процедуры (вид закупки/аукциона)."""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class ProcedureType(BaseModel):
    """Справочник типов процедур."""

    __tablename__ = "procedure_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    procedures = relationship("Procedure", back_populates="procedure_type")

    def __repr__(self) -> str:
        return f"<ProcedureType id={self.id} name={self.name} active={self.is_active}>"
