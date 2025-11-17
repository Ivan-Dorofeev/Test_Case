from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.signature import DigitalSignature
from app.models.user import User
from app.schemas.signature import DigitalSignatureResponse
from app.services.eds.signature_service import DigitalSignatureService

router = APIRouter()


@router.post("/", response_model=DigitalSignatureResponse)
async def upload_signature(
    file: UploadFile = File(...),
    document_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DigitalSignature:
    try:
        file_content = await file.read()
        signature = DigitalSignatureService.create_signature(
            db=db,
            user_id=current_user.id,
            document_id=document_id,
            file_content=file_content,
            filename=file.filename or "unknown",
            content_type=file.content_type or "application/octet-stream",
        )
        return signature
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/", response_model=list[DigitalSignatureResponse])
def list_signatures(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[DigitalSignature]:
    return DigitalSignatureService.list_signatures(db, user_id=current_user.id)


@router.get("/{signature_id}", response_model=DigitalSignatureResponse)
def get_signature(
    signature_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DigitalSignature | None:
    signature = DigitalSignatureService.get_signature(db, signature_id)
    if not signature or signature.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="ЭЦП не найдена")
    return signature


@router.delete("/{signature_id}")
def delete_signature(
    signature_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict[str, str]:
    signature = DigitalSignatureService.get_signature(db, signature_id)
    if not signature or signature.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="ЭЦП не найдена")

    if not DigitalSignatureService.delete_signature(db, signature_id):
        raise HTTPException(status_code=500, detail="Ошибка при удалении ЭЦП")

    return {"message": "ЭЦП успешно удалена"}
