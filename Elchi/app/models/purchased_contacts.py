"""Покупка доступа к контактной информации через транзакцию."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class PurchasedContacts(BaseModel):
    """Факт покупки контакта пользователем, связанный с транзакцией."""

    __tablename__ = "purchased_contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contact_information.id", ondelete="SET NULL"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("transaction.id", ondelete="RESTRICT"), nullable=False)

    user = relationship("User")
    contact = relationship("ContactInformation")
    transaction = relationship("Transaction", back_populates="purchased_contacts")

    def __repr__(self) -> str:
        return (
            f"<PurchasedContacts id={self.id} user_id={self.user_id} "
            f"contact_id={self.contact_id} transaction_id={self.transaction_id}>"
        )
