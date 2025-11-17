"""Модель объявления и его связи с файлами, работами и откликами.

Хранит параметры объявления, ценовые диапазоны, ответственных лиц и статус.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus


class Announcement(BaseModel):
    """Объявление о закупке/работах.

    Содержит основную информацию, связи с контактами, компанией, файлами,
    типами работ, комментариями модератора и откликами.
    """

    __tablename__ = "announcement"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    new_field = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price_from = Column(Numeric(12, 2), nullable=False)
    price_to = Column(Numeric(12, 2), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    moderator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contact_information.id", ondelete="SET NULL"), nullable=True)
    status = Column(SQLEnum(AnnouncementStatus), nullable=False)
    closed_at = Column(DateTime, nullable=True)
    close_reason = Column(String(255), nullable=True)  # ограничение длины
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False)

    creator = relationship("User", foreign_keys=[creator_id])
    moderator = relationship("User", foreign_keys=[moderator_id])
    contact = relationship("ContactInformation")
    company = relationship("Company")
    files = relationship("AnnouncementFile", back_populates="announcement", cascade="all, delete-orphan")
    works = relationship("AnnouncementWorks", back_populates="announcement", cascade="all, delete-orphan")
    comments = relationship("ModeratorComment", back_populates="announcement")
    responses = relationship("AdsResponse", back_populates="announcement")

    def __repr__(self) -> str:
        return f"<Announcement id={self.id} name={self.name} type={self.type}>"
