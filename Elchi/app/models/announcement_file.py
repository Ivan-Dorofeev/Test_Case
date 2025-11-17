"""Модель связи объявления с загруженными файлами.
Содержит описание файла, привязанного к объявлению.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class AnnouncementFile(BaseModel):
    """Файл, прикреплённый к объявлению."""

    __tablename__ = "announcement_file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    announcement_id = Column(Integer, ForeignKey("announcement.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(Integer, ForeignKey("file.id", ondelete="CASCADE"), nullable=False)
    description = Column(String(255), nullable=True)

    announcement = relationship("Announcement", back_populates="files")
    file = relationship("File")

    def __repr__(self) -> str:
        return f"<AnnouncementFile id={self.id} announcement_id={self.announcement_id} file_id={self.file_id}>"
