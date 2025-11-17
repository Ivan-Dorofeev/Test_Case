"""Модель пользователя и связанные отношения.

Определяет таблицу `users`, базовые поля аккаунта, статусы и связи
с историей входов, командами, логами действий и балансом пользователя.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base as BaseModel
from app.models.enums.Enum_Model import CompanyUserRole


class User(BaseModel):
    """Пользователь системы.

    Хранит учетные данные и флаги доступа, а также агрегирует связанные
    сущности: историю входов, созданные команды, логи действий и баланс.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    role = Column(SQLEnum(CompanyUserRole, native_enum=False), nullable=False)

    deleted_at = Column(DateTime, nullable=True)  # soft-delete

    login_history = relationship("LoginHistory", back_populates="user")
    teams = relationship("WorkersTeam", back_populates="creator")
    action_logs = relationship("ActionLog", back_populates="user")
    balance = relationship("Balance", back_populates="user", uselist=False, cascade="all, delete-orphan")

    created_adv_records = relationship(
        "AdvRecords", foreign_keys="AdvRecords.creator_id", back_populates="creator", cascade="all, delete-orphan"
    )

    moderator_adv_records = relationship(
        "AdvRecords", foreign_keys="AdvRecords.moderator_id", back_populates="moderator"
    )
    signatures = relationship("DigitalSignature", back_populates="user")

    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def soft_delete(self) -> None:
        self.deleted_at = datetime.utcnow()
        self.is_active = False

    def __repr__(self) -> str:
        return f"<User {self.email}>"
