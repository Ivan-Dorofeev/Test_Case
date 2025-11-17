"""Справочник регионов для привязки компаний и объявлений."""

from sqlalchemy import Column, Integer, String

from app.database.database import Base as BaseModel


class Region(BaseModel):
    """Регион с названием и координатами (опционально)."""

    __tablename__ = "region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    coordinates = Column(String(50), nullable=True)

    def __repr__(self) -> str:
        return f"<Region id={self.id} name={self.name}>"
