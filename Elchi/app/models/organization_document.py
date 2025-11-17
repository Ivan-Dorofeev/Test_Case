from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base as BaseModel


class OrganizationDocument(BaseModel):
    __tablename__ = "organization_document"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    file_url = Column(String)  # S3
    title = Column(String, nullable=False)  # например: "Копия устава"
    doc_type = Column(String)  # "org_doc", "certificate", "sbrs"

    signatures = relationship("DigitalSignature", back_populates="document")
