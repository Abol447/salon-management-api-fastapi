from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.models.owner import Owner
from app.models.user import User
from app.core.messages import messages
from app.schemas.response import ResponseSchema
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserCreateIn
)
from app.models.role import Role
from app.models.customer import Customer
from app.services.user_service import UserService
from app.api.wallet_router import get_wallet_service
from app.repositories.base.CRUDBase import CRUDBase

from app.api.discount_router import get_discount_service

router = APIRouter(prefix="/user", tags=["user"])


def get_user_service() -> UserService:
    repo = CRUDBase(User)
    role_repo = CRUDBase(Role)
    customer_repo = CRUDBase(Customer)
    owner_repo = CRUDBase(Owner)
    wallet = get_wallet_service()
    discount_service = get_discount_service()
    return UserService(
        repo, role_repo, customer_repo, owner_repo, wallet, discount_service
    )


@router.post("", response_model=ResponseSchema[UserResponse])
def create_user(
    user_data: UserCreateIn,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    data = service.create(db, user_data)
    return ResponseSchema(data=data, message=messages.USER_CREATED)


@router.get("", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db), service: UserService = Depends(get_user_service)
):
    return service.get_all(db)


@router.get("/me", response_model=UserResponse)
def get_user(
    user : dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.get(db, user["sub"])


@router.patch("/update/me", response_model=ResponseSchema[UserResponse])
def update_user(
    user_data: UserUpdate,
    user : dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    data = service.update(db, user["sub"], user_data)
    return ResponseSchema(data=data, message=messages.UPDATED)


@router.delete("/{user_id}", response_model=ResponseSchema[UserResponse])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    data = service.delete(db, user_id)
    return ResponseSchema(data=data, message=messages.DELETED)
