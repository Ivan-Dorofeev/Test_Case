from sqlalchemy import Column, Integer, String

from app.database.database import Base as BaseModel


class OrganizationUserPreferences(BaseModel):
    __tablename__ = "organization_user_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    last_director_fio = Column(String)
    last_contact_fio = Column(String)
    last_phone = Column(String)
    last_email = Column(String)
