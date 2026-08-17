from app.services.owner_service import OwnerService
from app.models.owner import Owner
from app.schemas.owner import (
    OwnerCreate,
    OwnerUpdate,
    OwnerResponse,
)
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.response import ResponseSchema
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.messages import messages
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/owner", tags=["owner"])


def get_service():
    repo = CRUDBase(Owner)
    return OwnerService(repo)


@router.post("", response_model=ResponseSchema[OwnerResponse])
def create(
    data_in: OwnerCreate,
    db: Session = Depends(get_db),
    service: OwnerService = Depends(get_service),
):
    data = service.create(db, data_in)

    return ResponseSchema(message=messages.CREATED, data=data)


@router.get("", response_model=ResponseSchema[list[OwnerResponse]])
def get_all(
    db: Session = Depends(get_db),
    service: OwnerService = Depends(get_service),
):
    data = service.get_all(db)

    return ResponseSchema(message=messages.GET_ALL, data=data)


@router.get("/{owner_id}", response_model=ResponseSchema[OwnerResponse])
def get(
    owner_id: int,
    db: Session = Depends(get_db),
    service: OwnerService = Depends(get_service),
):
    data = service.get(db, owner_id)

    return ResponseSchema(message=messages.GET_ALL, data=data)


@router.put("/{owner_id}", response_model=ResponseSchema[OwnerResponse])
def update(
    owner_id: int,
    data_in: OwnerUpdate,
    db: Session = Depends(get_db),
    service: OwnerService = Depends(get_service),
):
    data = service.update(db, owner_id, data_in)

    return ResponseSchema(message=messages.UPDATED, data=data)


@router.delete("/{owner_id}", response_model=ResponseSchema[OwnerResponse])
def delete(
    owner_id: int,
    db: Session = Depends(get_db),
    service: OwnerService = Depends(get_service),
):
    data = service.delete(db, owner_id)

    return ResponseSchema(message=messages.DELETED, data=data)
