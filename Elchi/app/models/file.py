"""Файлы в файловом хранилище и их типы/доступ."""

from sqlalchemy import Boolean, Column, Integer, String

from app.database.database import Base as BaseModel


class File(BaseModel):
    """Метаинформация о файле (путь, тип, приватность)."""

    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(1024), nullable=False)
    type = Column(String(50), nullable=False)
    is_private = Column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"<File id={self.id} path={self.path} type={self.type}>"
