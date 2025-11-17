from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.organization import (
    OrganizationResponse,
    OrganizationShortResponse,
    OrganizationStatusResponse,
    OrganizationStep1Request,
    OrganizationStep1Response,
    OrganizationStep2Request,
    OrganizationStep2Response,
    OrganizationStep3Request,
    OrganizationStep3Response,
    OrganizationStep4Request,
    OrganizationStep4Response,
    OrganizationStep5Request,
    OrganizationStep5Response,
    OrganizationStep6Request,
    OrganizationStep6Response,
    OrganizationStep7Request,
    OrganizationStep7Response,
    OrganizationStep8Request,
    OrganizationStep8Response,
)
from app.services.organization_service import OrganizationService

router = APIRouter()


@router.get(
    "/", response_model=List[OrganizationShortResponse], summary="Получить список всех организаций пользователя"
)
def get_my_organizations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Получить список всех организаций пользователя"""
    organizations = OrganizationService.get_by_user(db, user_id=current_user.id)
    return organizations


@router.post("/", response_model=OrganizationResponse, summary="Создать новую организацию")
def create_organization(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Создать новую организацию"""
    org = OrganizationService.create_draft(db, user_id=current_user.id)
    return org


@router.get("/{org_id}", response_model=OrganizationResponse, summary="Получить организацию по ID")
def get_organization(org_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Получить организацию по ID (все шаги)"""
    org = OrganizationService.get_by_id_and_user(db, org_id=org_id, user_id=current_user.id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.put("/organizations/{org_id}", response_model=OrganizationResponse, summary="Обновить организации по ID")
async def update_organization_endpoint(org_id: int, org_update: OrganizationResponse, db: Session = Depends(get_db)):
    """Обновление организации по ID"""
    updated_org = OrganizationService.update_organization(db, org_id, org_update)
    if updated_org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return updated_org


@router.put(
    "/{org_id}/step/1",
    response_model=OrganizationStep1Response,
    summary="Сохранить шаг 1: Основная информация и логотип",
)
def save_step_1(
    org_id: int,
    data: OrganizationStep1Request,
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 1: Основная информация и логотип"""
    org = OrganizationService.save_step_1(db, org_id=org_id, user_id=current_user.id, data=data, logo_file=logo)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.put("/{org_id}/step/2", response_model=OrganizationStep2Response, summary="Сохранить шаг 2: Адреса")
def save_step_2(
    org_id: int,
    data: OrganizationStep2Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 2: Адреса"""
    org = OrganizationService.save_step_2(db, org_id=org_id, user_id=current_user.id, data=data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.put(
    "/{org_id}/step/3", response_model=OrganizationStep3Response, summary="Сохранить шаг 3: Контактная информация"
)
def save_step_3(
    org_id: int,
    data: OrganizationStep3Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 3: Контактная информация"""
    org = OrganizationService.save_step_3(db, org_id=org_id, user_id=current_user.id, data=data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.put(
    "/{org_id}/step/4", response_model=OrganizationStep4Response, summary="Сохранить шаг 4: Деятельность и бригады"
)
def save_step_4(
    org_id: int,
    data: OrganizationStep4Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 4: Деятельность и бригады"""
    org = OrganizationService.save_step_4(db, org_id=org_id, user_id=current_user.id, data=data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.put("/{org_id}/step/5", response_model=OrganizationStep5Response, summary="Сохранить шаг 5: Примеры работ")
def save_step_5(
    org_id: int,
    data: OrganizationStep5Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 5: Примеры работ"""
    org = OrganizationService.save_step_5(db, org_id=org_id, user_id=current_user.id, data=data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.put(
    "/{org_id}/step/6",
    response_model=OrganizationStep6Response,
    summary="Сохранить шаг 6: Документы (обязательный минимум 1)",
)
def save_step_6(
    org_id: int,
    data: OrganizationStep6Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 6: Документы (обязательный минимум 1)"""
    org = OrganizationService.save_step_6(db, org_id=org_id, user_id=current_user.id, data=data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.put(
    "/{org_id}/step/7", response_model=OrganizationStep7Response, summary="Сохранить шаг 7: Сертификаты и лицензии"
)
def save_step_7(
    org_id: int,
    data: OrganizationStep7Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 7: Сертификаты и лицензии"""
    org = OrganizationService.save_step_7(db, org_id=org_id, user_id=current_user.id, data=data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.put("/{org_id}/step/8", response_model=OrganizationStep8Response, summary="Сохранить шаг 8: СБРС")
def save_step_8(
    org_id: int,
    data: OrganizationStep8Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Сохранить шаг 8: СБРС"""
    org = OrganizationService.save_step_8(db, org_id=org_id, user_id=current_user.id, data=data)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not editable")
    return org


@router.post(
    "/{org_id}/submit", response_model=OrganizationStatusResponse, summary="Отправить организацию на модерацию"
)
def submit_for_moderation(org_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Отправить организацию на модерацию"""
    org = OrganizationService.submit_for_moderation(db, org_id=org_id, user_id=current_user.id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found or not in draft")
    return {"status": org.status, "rejection_reasons": org.rejection_reasons or []}


@router.delete(
    "/{org_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить черновик (только если статус draft)"
)
def delete_draft(org_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Удалить черновик (только если статус draft)"""
    success = OrganizationService.delete_draft(db, org_id=org_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Draft not found or cannot be deleted")
    return None
