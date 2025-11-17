"""Тип позиции спецификации процедуры."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class SpecificationType(BaseModel):
    """Справочник типов спецификаций для процедур."""

    __tablename__ = "specification_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    creator = relationship("User")
    specifications = relationship("ProcedureSpecification", back_populates="type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<SpecificationType id={self.id} name={self.name}>"
