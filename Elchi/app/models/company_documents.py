"""Документы компании и их типы."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class CompanyDocuments(BaseModel):
    """Описание документа компании (тип, привязка к компании)."""

    __tablename__ = "company_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)  # можно Enum для фиксированных типов

    files = relationship("CompanyDocumentsFile", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<CompanyDocuments id={self.id} company_id={self.company_id} type={self.type}>"
