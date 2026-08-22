from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.db.database import get_db
from fastapi import APIRouter, Depends
from app.schemas.auth import LoginResponse, LoginSchema, LogOutSchema
from sqlalchemy.orm import Session
from app.schemas.token import refresh_token
from app.core.messages import messages
from app.schemas.response import ResponseSchema

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service():
    repo = AuthRepository()
    return AuthService(repo)


@router.post("/login", response_model=ResponseSchema[LoginResponse])
def login(
    user_data: LoginSchema,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    data = service.login_service(db, user_data)

    return ResponseSchema(data=data, message=messages.LOGIN_SUCCESS)


@router.post("/logout", response_model=ResponseSchema[None | str])
def logout(
    refresh_token: LogOutSchema,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    data = service.logout_service(db, refresh_token)

    return ResponseSchema(data=data, message=messages.LOGOUT_SUCCESS)


@router.post("/refresh", response_model=ResponseSchema[LoginResponse])
def refresh_access_token(
    data: refresh_token,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    response = service.refresh_access_token_service(db, data.refresh_token)

    return ResponseSchema(data=response, message=messages.TOKEN_REFRESHED)
