"""Справочник типов работ для объявлений."""

from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.database import Base as BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus


class AnnouncementWorkType(BaseModel):
    """Тип работ, используемый в объявлениях."""

    __tablename__ = "announcement_work_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    status = Column(SQLEnum(AnnouncementStatus), nullable=False)

    works = relationship("AnnouncementWorks", back_populates="work_type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<AnnouncementWorkType id={self.id} name={self.name}>"
