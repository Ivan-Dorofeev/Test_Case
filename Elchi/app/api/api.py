from fastapi import APIRouter

from app.api.endpoints import (
    announcements,
    company,
    company_comment,
    company_users,
    notifications,
    organizations,
    s3,
    signatures, procedure_comment, procedure,
)
from app.api.User import login, password, register, users

api_router = APIRouter()

# Auth модули
api_router.include_router(register.router, prefix="/auth", tags=["registration"])
api_router.include_router(login.router, prefix="/auth", tags=["login"])
api_router.include_router(password.router, prefix="/auth", tags=["password"])

# Общие роуты пользователей
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(s3.router, prefix="/files", tags=["files"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(announcements.router, prefix="/announcements", tags=["announcements"])
api_router.include_router(signatures.router, prefix="/signatures", tags=["signatures"])
api_router.include_router(company.router, prefix="/companies", tags=["companies"])

api_router.include_router(procedure.router, prefix="/procedures", tags=["procedures"])
api_router.include_router(company_comment.router, prefix="/comments/company", tags=["Company Comments"])
api_router.include_router(procedure_comment.router, prefix="/comments/procedure", tags=["Procedure Comments"])
api_router.include_router(company_users.router, prefix="/companies_user", tags=["Company Users"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
