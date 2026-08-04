from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.role import RoleResponse, RoleCreate, RoleUpdate
from app.services.role_service import RoleService
from app.db.database import get_db


router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


def get_service() -> RoleService:
    repo = CRUDBase(Role)
    return RoleService(repo)


@router.post(
    "",
    response_model=RoleResponse,
    status_code=201
)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service)
):
    return service.create(db, role_data)


@router.get(
    "/{role_id}",
    response_model=RoleResponse
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service)
):
    return service.get_by_id(db, role_id)


@router.get(
    "",
    response_model=list[RoleResponse]
)
def get_roles(
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service)
):
    return service.get_all(db)


@router.put(
    "/{role_id}",
    response_model=RoleResponse
)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service)
):
    return service.update(db, role_id, role_data)


@router.delete(
    "/{role_id}",
    status_code=204
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    service: RoleService = Depends(get_service)
):
    service.delete(db, role_id)

    return None