from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.role import RoleResponse, RoleCreate, RoleUpdate
from app.services.role_service import RoleService
from app.db.database import get_db
from app.core.messages import messages
from app.schemas.response import ResponseSchema

router = APIRouter(prefix="/roles", tags=["roles"])


def get_service() -> RoleService:
    repo = CRUDBase(Role)
    return RoleService(repo)


@router.post("", response_model=ResponseSchema[RoleResponse], status_code=201)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service),
):
    data = service.create(db, role_data)

    return ResponseSchema(data=data, message=messages.ROLE_CREATED)


@router.get("/{role_id}", response_model=ResponseSchema[RoleResponse])
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service),
):
    data = service.get_by_id(db, role_id)

    return ResponseSchema(data=data, message=messages.GET_ALL)


@router.get("", response_model=ResponseSchema[list[RoleResponse]])
def get_roles(
    db: Session = Depends(get_db), service: RoleService = Depends(get_service)
):
    data = service.get_all(db)

    return ResponseSchema(data=data, message=messages.GET_ALL)


@router.put("/{role_id}", response_model=ResponseSchema[RoleResponse])
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service),
):
    data = service.update(db, role_id, role_data)

    return ResponseSchema(data=data, message=messages.ROLE_UPDATED)


@router.delete("/{role_id}", response_model=ResponseSchema[RoleResponse])
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service),
):
    data = service.delete(db, role_id)

    return ResponseSchema(data=data, message=messages.ROLE_DELETED)
