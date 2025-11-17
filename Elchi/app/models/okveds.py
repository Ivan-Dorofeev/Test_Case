"""Справочник кодов ОКВЭД."""

from sqlalchemy import Boolean, Column, Integer, String

from app.database.database import Base as BaseModel


class Okveds(BaseModel):
    """Код и наименование ОКВЭД с признаком активности."""

    __tablename__ = "okveds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    okved_id = Column(String(15), nullable=False)
    okved_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Okveds id={self.id} code={self.okved_id} name={self.okved_name} active={self.is_active}>"
