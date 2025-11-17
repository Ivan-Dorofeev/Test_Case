"""Роутер для работы с компаниями."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.company import (
    CompanyCreate,
    CompanyReadFull,
    CompanyReadShort,
    CompanyUpdate,
)
from app.services.company_service import CompanyService

router = APIRouter()


# -------------------- CREATE --------------------
@router.post("/", response_model=CompanyReadFull, summary="Создать компанию")
def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyReadFull:
    """Создаёт новую компанию."""
    return CompanyReadFull.model_validate(CompanyService.create_company(db, data, current_user))


# -------------------- READ --------------------
@router.get("/{company_id}", response_model=CompanyReadFull, summary="Получить компанию по ID")
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyReadFull:
    """Возвращает полную информацию о компании по `company_id`."""
    return CompanyReadFull.model_validate(CompanyService.get_company(db, company_id, current_user))


@router.get("/", response_model=List[CompanyReadShort], summary="Список компаний с фильтрацией и поиском")
def list_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    include_deleted: bool = Query(False, description="Показывать удалённые компании"),
    status: Optional[str] = Query(None, description="Фильтр по статусу компании"),
    type: Optional[int] = Query(None, description="Фильтр по типу компании"),
    is_public: Optional[bool] = Query(None, description="Фильтр по публичности компании"),
    search: Optional[str] = Query(None, description="Поиск по INN, OGRN или имени компании"),
) -> List[CompanyReadShort]:
    """Возвращает список компаний с возможностью фильтрации и поиска."""
    companies = CompanyService.list_companies(
        db=db,
        current_user=current_user,
        include_deleted=include_deleted,
        status=status or "",
        type=type or 0,
        is_public=is_public or False,
        search=search or "",
    )
    return [CompanyReadShort.model_validate(c) for c in companies]


# -------------------- UPDATE --------------------
@router.patch("/{company_id}", response_model=CompanyReadFull, summary="Обновить компанию")
def update_company(
    company_id: int,
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyReadFull:
    """Обновляет компанию."""
    return CompanyReadFull.model_validate(CompanyService.update_company(db, company_id, data, current_user))


# -------------------- DELETE --------------------
@router.delete("/{company_id}", summary="Удалить компанию (soft/hard)")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    hard: bool = Query(False, description="Если True — удаление безвозвратно"),
) -> dict[str, str]:
    """Удаляет компанию (soft/hard)."""
    return CompanyService.delete_company(db, company_id, current_user, hard)


# -------------------- RESTORE --------------------
@router.post("/{company_id}/restore", response_model=CompanyReadFull, summary="Восстановить удалённую компанию")
def restore_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> CompanyReadFull:
    """Восстанавливает удалённую компанию."""
    return CompanyReadFull.model_validate(CompanyService.restore_company(db, company_id, current_user))
