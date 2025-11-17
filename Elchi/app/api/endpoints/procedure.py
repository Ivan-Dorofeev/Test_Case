# app/api/endpoints/procedure_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import procedure as procedure_crud
from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User # Импортируем модель User для типизации current_user
from app.schemas import procedure as procedure_schemas # Импортируем схемы

router = APIRouter()


@router.get("/{procedure_id}", response_model=procedure_schemas.ProcedureReadFull, summary="Получить тендер по ID")
def get_procedure(
    procedure_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> procedure_schemas.ProcedureReadFull:
    """
    Получает информацию об одной процедуре по её ID.
    """
    procedure = procedure_crud.get(db, id=procedure_id)
    if not procedure:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Procedure not found")
    return procedure


@router.get("/", response_model=List[procedure_schemas.ProcedureReadFull], summary="Получить список тендеров")
def list_procedures(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # Проверяем активного пользователя
) -> List[procedure_schemas.ProcedureReadFull]:
    """
    Получает список процедур с пагинацией.
    """
    procedures = procedure_crud.get_multi(db, skip=skip, limit=limit)
    return procedures
