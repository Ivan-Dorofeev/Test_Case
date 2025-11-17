"""Записи рекламных размещений и их модерации/транзакций."""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class AdvRecords(BaseModel):
    __tablename__ = "adv_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("file.id", ondelete="SET NULL"), nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="SET NULL"), nullable=True)
    link = Column(String(512), nullable=True)
    moderator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    place_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    transaction_id = Column(Integer, ForeignKey("transaction.id", ondelete="SET NULL"), nullable=True)

    asset = relationship("File")
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_adv_records")
    moderator = relationship("User", foreign_keys=[moderator_id], back_populates="moderator_adv_records")
    company = relationship("Company")
    transaction = relationship("Transaction")

    def __repr__(self) -> str:
        return (
            f"<AdvRecords id={self.id} asset_id={self.asset_id} "
            f"creator_id={self.creator_id} active={self.is_active}>"
        )
