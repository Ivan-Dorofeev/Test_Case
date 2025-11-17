"""Журнал действий пользователей по сущностям системы."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel
from app.models.enums.Enum_Model import ActionType


class ActionLog(BaseModel):
    """Запись о действии пользователя над сущностью.

    Фиксирует тип действия, идентификатор сущности и время создания записи.
    """

    __tablename__ = "action_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True)
    entity_name = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    action_type = Column(SQLEnum(ActionType), nullable=False)  # ограничение через Enum

    user = relationship("User", back_populates="action_logs")

    def __repr__(self) -> str:
        return (
            f"<ActionLog user_id={self.user_id} entity={self.entity_name}:{self.entity_id} action={self.action_type}>"
        )
