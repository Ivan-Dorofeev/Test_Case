"""Связь документов компании с файлами в хранилище."""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class CompanyDocumentsFile(BaseModel):
    """Файл, прикреплённый к документу компании."""

    __tablename__ = "company_documents_file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    documents_id = Column(Integer, ForeignKey("company_documents.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(Integer, ForeignKey("file.id", ondelete="CASCADE"), nullable=False)

    document = relationship("CompanyDocuments", back_populates="files")
    file = relationship("File")

    __table_args__ = (UniqueConstraint("documents_id", "file_id", name="uq_company_documents_file"),)

    def __repr__(self) -> str:
        return f"<CompanyDocumentsFile id={self.id} documents_id={self.documents_id} file_id={self.file_id}>"
