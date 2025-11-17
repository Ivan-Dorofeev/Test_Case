"""Модель компании и связанные пользовательские роли/контакты.
Описывает юридическое лицо, его реквизиты, контактных и ответственных пользователей.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class Company(BaseModel):
    """Компания-заказчик или исполнитель.

    Содержит основные реквизиты, адреса, контактные данные и ссылки на
    пользователей-участников (основатель, контактное лицо, проверяющий).
    """

    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # можно Enum
    full_name = Column(String(500), nullable=False)
    type = Column(Integer, nullable=False)
    INN = Column(String(12), nullable=False, unique=True)
    KPP = Column(String(9), nullable=False)
    OGRN = Column(String(15), nullable=False, unique=True)
    OKTMO = Column(String(8), nullable=False)
    founder_type = Column(String(50), nullable=True)
    founder_full_name = Column(String(255), nullable=True)
    founder_inn = Column(String(12), nullable=False)
    founder_snils = Column(String(11), nullable=False)
    founder_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    zip = Column(String(10), nullable=False)
    legal_address = Column(String(512), nullable=False)
    physical_address = Column(String(512), nullable=False)
    site_link = Column(String(512), nullable=True)
    contact_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    contact_user_name = Column(String(255), nullable=True)
    contact_user_job_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    sbrs = Column(Boolean, nullable=False, default=False)
    verify_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_public = Column(Boolean, nullable=False, default=True)

    deleted_at = Column(DateTime, nullable=True)  # soft-delete

    # Связи
    founder = relationship("User", foreign_keys=[founder_id])
    contact_user = relationship("User", foreign_keys=[contact_user_id])
    verifier = relationship("User", foreign_keys=[verify_by_id])

    def __repr__(self) -> str:
        return f"<Company id={self.id} name={self.name} INN={self.INN}>"
