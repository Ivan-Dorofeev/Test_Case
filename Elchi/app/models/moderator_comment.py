"""Комментарии модератора к объявлениям."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import AnnouncementStatus


class ModeratorComment(BaseModel):
    """Комментарий модератора по объявлению и его статусу."""

    __tablename__ = "moderator_comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    moderator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    announcement_id = Column(Integer, ForeignKey("announcement.id", ondelete="SET NULL"), nullable=True)
    text = Column(Text, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    status = Column(SQLEnum(AnnouncementStatus), nullable=False)

    moderator = relationship("User")
    announcement = relationship("Announcement", back_populates="comments")

    def __repr__(self) -> str:
        return (
            f"<ModeratorComment id={self.id} announcement_id={self.announcement_id} "
            f"moderator_id={self.moderator_id} status={self.status}>"
        )
