from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base as BaseModel


class OrganizationWorkExample(BaseModel):
    __tablename__ = "organization_work_examples"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    image_url = Column(String, nullable=False)  # ссылка на изображение в S3
    description = Column(Text)  # описание выполненной работы
    organization = relationship("Organization", back_populates="work_examples")
