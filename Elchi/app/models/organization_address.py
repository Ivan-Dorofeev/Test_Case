from sqlalchemy import Column, ForeignKey, Integer, String

from app.database.database import Base as BaseModel


class OrganizationAddress(BaseModel):
    __tablename__ = "organization_addresses"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    address_type = Column(String)  # "legal", "physical", "mailing"
    address = Column(String, nullable=False)
