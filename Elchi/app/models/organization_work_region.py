from sqlalchemy import Column, ForeignKey, Integer, String

from app.database.database import Base as BaseModel


class OrganizationWorkRegion(BaseModel):
    __tablename__ = "organization_work_region"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    region = Column(String, nullable=False)  # например: "Свердловская область"
