"""Отклик пользователя на объявление."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus


class AdsResponse(BaseModel):
    """Связь пользователя с объявлением, отражающая факт отклика."""

    __tablename__ = "ads_response"

    id = Column(Integer, primary_key=True, autoincrement=True)
    announcement_id = Column(Integer, ForeignKey("announcement.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    view_at = Column(DateTime, default=func.now(), nullable=False)
    status = Column(SQLEnum(AnnouncementStatus, name="ads_response_status"), nullable=False)

    announcement = relationship("Announcement", back_populates="responses")
    user = relationship("User")

    def __repr__(self) -> str:
        return (
            f"<AdsResponse id={self.id} announcement_id={self.announcement_id} "
            f"user_id={self.user_id} status={self.status}>"
        )
