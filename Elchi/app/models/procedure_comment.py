# app/models/procedure_comment.py
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base_class import BaseModel


class ProcedureComment(BaseModel):
    """Комментарий пользователя к тендеру"""

    __tablename__ = "procedure_comment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    procedure_id = Column(Integer, ForeignKey("procedure.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", backref="procedure_comments")
    procedure = relationship("Procedure", backref="comments")


    def __repr__(self) -> str:
        return f"<ProcedureComment id={self.id} procedure_id={self.procedure_id} user_id={self.user_id}>"

