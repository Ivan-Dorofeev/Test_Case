"""Справочник профессий/должностей и их связь с командами."""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base as BaseModel


class Jobs(BaseModel):
    """Профессия/должность, используемая для формирования команд."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    teams = relationship("TeamJobs", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Job id={self.id} name={self.name}>"
