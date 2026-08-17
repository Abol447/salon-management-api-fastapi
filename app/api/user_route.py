from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.owner import Owner
from app.models.user import User
from app.core.messages import messages
from app.schemas.response import ResponseSchema
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.models.role import Role
from app.models.customer import Customer
from app.services.user_service import UserService

from app.repositories.base.CRUDBase import CRUDBase

router = APIRouter(prefix="/user", tags=["user"])


def get_user_service() -> UserService:
    repo = CRUDBase(User)
    role_repo = CRUDBase(Role)
    customer_repo = CRUDBase(Customer)
    owner_repo = CRUDBase(Owner)
    return UserService(repo, role_repo, customer_repo, owner_repo)


@router.post("", response_model=ResponseSchema[UserResponse])
def create_user(
    user_data: UserCreate,
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


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.get(db, user_id)


@router.patch("/{user_id}", response_model=ResponseSchema[UserResponse])
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    data = service.update(db, user_id, user_data)
    return ResponseSchema(data=data, message=messages.UPDATED)


@router.delete("/{user_id}", response_model=ResponseSchema[UserResponse])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    data = service.delete(db, user_id)
    return ResponseSchema(data=data, message=messages.DELETED)
