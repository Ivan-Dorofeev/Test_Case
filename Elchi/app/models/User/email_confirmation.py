# app/models/email_confirmation.py
from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.database import Base


class EmailConfirmation(Base):
    __tablename__ = "email_confirmations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    code = Column(String(10), nullable=False)
    purpose = Column(String, nullable=False, default="registration")
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=False)
    attempts = Column(Integer, default=0)

    user = relationship("User", backref="email_confirmations")

    @staticmethod
    def expiry(minutes: int = 10) -> datetime:
        return datetime.utcnow() + timedelta(minutes=minutes)
