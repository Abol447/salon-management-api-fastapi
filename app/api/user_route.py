from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

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
    return UserService(repo, role_repo, customer_repo)


@router.post("", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.create(db, user_data)


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


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.update(db, user_id, user_data)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.delete(db, user_id)
