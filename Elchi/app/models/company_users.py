"""Участники компании и их роли."""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus, CompanyUserRole


class CompanyUsers(BaseModel):
    """Связь пользователя с компанией и его ролью в ней."""

    __tablename__ = "company_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="RESTRICT"), nullable=False)
    role = Column(SQLEnum(CompanyUserRole), nullable=False)
    approve_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(SQLEnum(AnnouncementStatus, name="company_user_status"), nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    approver = relationship("User", foreign_keys=[approve_by_id])
    company = relationship("Company")

    __table_args__ = (UniqueConstraint("user_id", "company_id", name="uq_company_user"),)

    def __repr__(self) -> str:
        return f"<CompanyUsers id={self.id} user_id={self.user_id} company_id={self.company_id} role={self.role}>"
