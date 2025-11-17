"""Документы, относящиеся к процедуре."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class ProcedureDocuments(BaseModel):
    """Файл документа, привязанный к процедуре и его тип."""

    __tablename__ = "procedure_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_id = Column(Integer, ForeignKey("procedure.id", ondelete="SET NULL"), nullable=True)
    file_id = Column(Integer, ForeignKey("file.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)

    procedure = relationship("Procedure", back_populates="documents")
    file = relationship("File")

    def __repr__(self) -> str:
        return (
            f"<ProcedureDocuments id={self.id} procedure_id={self.procedure_id} "
            f"file_id={self.file_id} type={self.type}>"
        )
