"""Спецификация (позиция) в процедуре с количеством и ценой."""

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class ProcedureSpecification(BaseModel):
    """Позиция спецификации процедуры и её тип."""

    __tablename__ = "procedure_specification"

    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_id = Column(Integer, ForeignKey("procedure.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    type_id = Column(Integer, ForeignKey("specification_type.id", ondelete="RESTRICT"), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)

    procedure = relationship("Procedure", back_populates="specifications")
    type = relationship("SpecificationType")

    def __repr__(self) -> str:
        return (
            f"<ProcedureSpecification id={self.id} procedure_id={self.procedure_id} "
            f"name={self.name} type_id={self.type_id} price={self.price}>"
        )
