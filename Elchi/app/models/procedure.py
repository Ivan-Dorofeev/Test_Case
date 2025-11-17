"""Модель процедуры и ее временные параметры/этапы.

Содержит ссылки на контакты, создателя, тип процедуры и связанные сущности
(пользователи, спецификации, документы, заявки), а также даты этапов.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.base_class import BaseModel


class Procedure(BaseModel):
    """Процедура закупки/аукциона с этапами и участниками.

    Описывает место и сроки комиссий, видимость, требования и ключевые даты
    (начало/окончание подачи заявок, этапы аукциона и др.).
    """

    __tablename__ = "procedure"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contact_information.id", ondelete="SET NULL"), nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    procedure_type_id = Column(Integer, ForeignKey("procedure_type.id", ondelete="RESTRICT"), nullable=False)
    commission_work_place = Column(String(255), nullable=False)
    delivery_place = Column(String(255), nullable=False)
    minimal_sbrs_rating = Column(Integer, nullable=True)
    visible_type = Column(String(255), nullable=False)
    second_step_enable = Column(Boolean, nullable=False, default=False)
    start_date = Column(DateTime, nullable=True)
    final_create_request_date = Column(DateTime, nullable=True)
    commission_work_start_date = Column(DateTime, nullable=True)
    commission_work_final_date = Column(DateTime, nullable=True)
    sign_required = Column(Boolean, nullable=False, default=False)
    auction_start_date = Column(DateTime, nullable=True)
    auction_final_date = Column(DateTime, nullable=True)
    auction_resolution_start_date = Column(DateTime, nullable=True)
    auction_resolution_final_date = Column(DateTime, nullable=True)

    contact = relationship("ContactInformation")
    creator = relationship("User")
    procedure_type = relationship("ProcedureType")
    users = relationship("ProcedureUser", back_populates="procedure")
    specifications = relationship("ProcedureSpecification", back_populates="procedure", cascade="all, delete-orphan")
    documents = relationship("ProcedureDocuments", back_populates="procedure")
    requests = relationship("ProcedureRequest", back_populates="procedure")

    def __repr__(self) -> str:
        return (
            f"<Procedure id={self.id} creator_id={self.creator_id} "
            f"type_id={self.procedure_type_id} start={self.start_date} end={self.final_create_request_date}>"
        )
