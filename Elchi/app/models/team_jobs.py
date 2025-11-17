"""Связь между командой и профессией (ролью)."""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class TeamJobs(BaseModel):
    """Привязка роли к конкретной команде рабочих."""

    __tablename__ = "team_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("workers_team.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)

    team = relationship("WorkersTeam", back_populates="jobs")
    job = relationship("Jobs", back_populates="teams")

    __table_args__ = (UniqueConstraint("team_id", "job_id", name="uq_team_job"),)

    def __repr__(self) -> str:
        return f"<TeamJobs id={self.id} team_id={self.team_id} job_id={self.job_id}>"
