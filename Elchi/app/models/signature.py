import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class SignatureType(str, enum.Enum):
    qualified = "qualified"
    unqualified = "unqualified"


class SignatureStatus(str, enum.Enum):
    uploaded = "uploaded"
    verified = "verified"
    invalid = "invalid"
    revoked = "revoked"


class DigitalSignature(BaseModel):
    __tablename__ = "digital_signatures"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("organization_document.id"), nullable=True)

    type = Column(SQLEnum(SignatureType, native_enum=False), nullable=False, default=SignatureType.qualified)
    status = Column(SQLEnum(SignatureStatus, native_enum=False), nullable=False, default=SignatureStatus.uploaded)

    file_url = Column(String, nullable=False)
    s3_object_name = Column(String, nullable=False)

    thumbprint = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    issuer = Column(String, nullable=True)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="signatures")
    document = relationship("OrganizationDocument", back_populates="signatures")
