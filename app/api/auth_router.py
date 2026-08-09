from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.db.database import get_db
from fastapi import APIRouter, Depends
from app.schemas.auth import LoginResponse, LoginSchema, LogOutSchema
from sqlalchemy.orm import Session
from app.schemas.token import refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service():
    repo = AuthRepository()
    return AuthService(repo)


@router.post("/login", response_model=LoginResponse)
def login(
    user_data: LoginSchema,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    return service.login_service(db, user_data)


@router.post("/logout")
def logout(
    refresh_token: LogOutSchema,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    return service.logout_service(db, refresh_token)


@router.post("/refresh", response_model=LoginResponse)
def refresh_access_token(
    data: refresh_token,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    return service.refresh_access_token_service(db, data.refresh_token)
