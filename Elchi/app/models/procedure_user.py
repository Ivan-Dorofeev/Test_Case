"""Участники процедуры и их роли/статусы."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus, CompanyUserRole


class ProcedureUser(BaseModel):
    """Пользователь, участвующий в процедуре, с ролью и статусом."""

    __tablename__ = "procedure_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_id = Column(Integer, ForeignKey("procedure.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(SQLEnum(CompanyUserRole), nullable=False)
    status = Column(SQLEnum(AnnouncementStatus), nullable=False)

    procedure = relationship("Procedure", back_populates="users")
    user = relationship("User")

    def __repr__(self) -> str:
        return (
            f"<ProcedureUser id={self.id} procedure_id={self.procedure_id} "
            f"user_id={self.user_id} role={self.role} status={self.status}>"
        )
