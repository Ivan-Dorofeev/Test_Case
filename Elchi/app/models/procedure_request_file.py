"""Файлы, приложенные к заявке по процедуре."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class ProcedureRequestFile(BaseModel):
    """Файл заявки: тип, автор и ссылка на файл."""

    __tablename__ = "procedure_request_file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("procedure_request.id", ondelete="CASCADE"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)
    file_id = Column(Integer, ForeignKey("file.id", ondelete="CASCADE"), nullable=False)

    request = relationship("ProcedureRequest", back_populates="files")
    creator = relationship("User")
    file = relationship("File")

    def __repr__(self) -> str:
        return (
            f"<ProcedureRequestFile id={self.id} request_id={self.request_id} "
            f"file_id={self.file_id} creator_id={self.creator_id} type={self.type}>"
        )
