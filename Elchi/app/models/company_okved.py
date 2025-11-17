"""Связь компании с кодами ОКВЭД."""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from app.database.base_class import BaseModel


class CompanyOkved(BaseModel):
    """Привязка компании к конкретному коду ОКВЭД."""

    __tablename__ = "company_okved"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    okved_id = Column(Integer, ForeignKey("okveds.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("company_id", "okved_id", name="uq_company_okved"),)

    def __repr__(self) -> str:
        return f"<CompanyOkved id={self.id} company_id={self.company_id} okved_id={self.okved_id}>"
