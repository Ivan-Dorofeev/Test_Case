"""Модель денежного баланса пользователя."""

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class Balance(BaseModel):
    """Баланс пользователя с поддержкой версионирования."""

    __tablename__ = "balance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    balance = Column(Numeric(12, 2), nullable=False, default=0, server_default="0")
    version = Column(Integer, nullable=False, default=1, server_default="1")

    user = relationship("User", back_populates="balance")

    __table_args__ = (
        CheckConstraint("balance >= 0", name="check_balance_non_negative"),
    )  # Проверка на положительность баланса, можно убрать если бизнес логика требует того

    def __repr__(self) -> str:
        return f"<Balance id={self.id} user_id={self.user_id} balance={self.balance} version={self.version}>"
