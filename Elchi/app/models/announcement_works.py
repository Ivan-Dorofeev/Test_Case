"""Связующая модель между объявлением и типом работ."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class AnnouncementWorks(BaseModel):
    """Связь объявления с конкретным видом работ."""

    __tablename__ = "announcement_works"

    id = Column(Integer, primary_key=True, autoincrement=True)
    announcement_id = Column(Integer, ForeignKey("announcement.id", ondelete="CASCADE"), nullable=False)
    work_type_id = Column(Integer, ForeignKey("announcement_work_type.id", ondelete="CASCADE"), nullable=False)

    announcement = relationship("Announcement", back_populates="works")
    work_type = relationship("AnnouncementWorkType", back_populates="works")

    def __repr__(self) -> str:
        return (
            f"<AnnouncementWorks id={self.id} announcement_id={self.announcement_id} work_type_id={self.work_type_id}>"
        )
