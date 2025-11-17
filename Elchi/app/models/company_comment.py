# app/models/company_comment.py
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class CompanyComment(BaseModel):
    """Комментарий пользователя к компании."""

    __tablename__ = "company_comment"

    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False)

    # связь с пользователем и компанией
    user = relationship("User", backref="company_comments")
    company = relationship("Company", backref="comments")

    # связь с ответом компании
    reply = relationship("CompanyReply", back_populates="comment", uselist=False)

    def __repr__(self) -> str:
        return f"<CompanyComment id={self.id} company_id={self.company_id} user_id={self.user_id}>"


class CompanyReply(BaseModel):
    """Ответ компании на комментарий."""

    __tablename__ = "company_reply"

    text = Column(Text, nullable=False)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    comment_id = Column(Integer, ForeignKey("company_comment.id", ondelete="CASCADE"), unique=True, nullable=False)

    # связь с комментарием
    comment = relationship("CompanyComment", back_populates="reply")

    def __repr__(self) -> str:
        return f"<CompanyReply id={self.id} company_id={self.company_id} comment_id={self.comment_id}>"
