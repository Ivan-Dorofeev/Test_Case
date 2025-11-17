"""Команда рабочих с описанием состава и инструментов."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class WorkersTeam(BaseModel):
    """Команда, созданная пользователем, с перечнем ролей и инструментов."""

    __tablename__ = "workers_team"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True)
    workers_number = Column(Integer, nullable=False)
    team_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    tools_list = Column(Text, nullable=True)

    creator = relationship("User", back_populates="teams")
    jobs = relationship("TeamJobs", back_populates="team", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<WorkersTeam id={self.id} type={self.team_type} workers={self.workers_number}>"
