from sqlalchemy import Column, ForeignKey, Integer, String

from app.database.database import Base as BaseModel


class OrganizationContactInfo(BaseModel):
    __tablename__ = "organization_contact_info"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    website = Column(String)
    contact_person_fio = Column(String)
    contact_person_position = Column(String)
    phone = Column(String)
    email = Column(String)
