from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.database.database import Base as BaseModel


class OrganizationTeam(BaseModel):
    __tablename__ = "organization_team"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    size = Column(Integer)
    team_type = Column(String)  # тип бригады
    work_type = Column(String)  # тип работ
    description = Column(Text)
    tools = Column(Text)  # оборудование и инструменты
