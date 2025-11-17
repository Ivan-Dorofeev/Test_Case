"""Финансовые транзакции пользователя и связанные покупки."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import TransactionStatus


class Transaction(BaseModel):
    """Транзакция с типом, статусом и произвольными метаданными."""

    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    type = Column(String, nullable=False)
    status = Column(SQLEnum(TransactionStatus), nullable=False)
    meta = Column(String, nullable=True)

    user = relationship("User")
    purchased_contacts = relationship("PurchasedContacts", back_populates="transaction")

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} user_id={self.user_id} type={self.type} status={self.status}>"
