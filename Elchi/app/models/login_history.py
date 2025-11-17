"""История входов пользователей в систему."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class LoginHistory(BaseModel):
    """Фиксация факта входа пользователя и его IP."""

    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True)
    ip = Column(String(45), nullable=False)

    # связь с User
    user = relationship("User", back_populates="login_history")

    def __repr__(self) -> str:
        return f"<LoginHistory user_id={self.user_id} ip={self.ip}>"
