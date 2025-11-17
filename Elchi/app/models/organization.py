from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.database import Base as BaseModel


class Organization(BaseModel):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # "legal_entity", "individual_entrepreneur"
    full_name = Column(String, nullable=False)
    short_name = Column(String)
    inn = Column(String, nullable=False)
    kpp = Column(String)
    ogrn = Column(String, nullable=False)
    okved = Column(String)
    oktmo = Column(String)
    director_fio = Column(String)
    director_position = Column(String)
    director_inn = Column(String)
    director_snils = Column(String)
    logo_url = Column(String)  # ссылка на файл в S3
    status = Column(String, default="draft")  # "draft", "moderation", "published", "rejected"
    rejection_reasons = Column(JSON)  # список причин отклонения
    sbrs_score = Column(Integer, default=0)  # СБРС баллы
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    work_examples = relationship("OrganizationWorkExample", back_populates="organization", cascade="all, delete-orphan")
