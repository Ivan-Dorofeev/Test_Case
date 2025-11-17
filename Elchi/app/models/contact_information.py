"""Контактная информация, связанная с пользователем и объявлениями."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus


class ContactInformation(BaseModel):
    """Контактные данные, используемые в процедурах и объявлениях."""

    __tablename__ = "contact_information"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(AnnouncementStatus, name="contact_status"), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)

    creator = relationship("User")
    announcements = relationship("Announcement", back_populates="contact")

    def __repr__(self) -> str:
        return f"<ContactInformation id={self.id} full_name={self.full_name}>"
