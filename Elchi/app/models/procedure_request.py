"""Заявка участника на участие в процедуре."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus


class ProcedureRequest(BaseModel):
    """Предложение компании/пользователя в рамках процедуры."""

    __tablename__ = "procedure_request"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="RESTRICT"), nullable=False)
    procedure_id = Column(Integer, ForeignKey("procedure.id", ondelete="SET NULL"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contact_information.id", ondelete="RESTRICT"), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    price_nds = Column(Integer, nullable=False)
    view_at = Column(DateTime, nullable=True)
    status = Column(SQLEnum(AnnouncementStatus), nullable=False)

    user = relationship("User")
    company = relationship("Company")
    procedure = relationship("Procedure", back_populates="requests")
    contact = relationship("ContactInformation")
    files = relationship("ProcedureRequestFile", back_populates="request", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"<ProcedureRequest id={self.id} user_id={self.user_id} "
            f"company_id={self.company_id} procedure_id={self.procedure_id} status={self.status}>"
        )
