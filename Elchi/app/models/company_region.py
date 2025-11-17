"""Связь компании с регионом деятельности."""

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from app.database.base_class import BaseModel


class CompanyRegion(BaseModel):
    """Привязка компании к региону."""

    __tablename__ = "company_region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("company_id", "region_id", name="uq_company_region"),)

    def __repr__(self) -> str:
        return f"<CompanyRegion id={self.id} company_id={self.company_id} region_id={self.region_id}>"
