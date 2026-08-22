from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.base.CRUDBase import CRUDBase
from app.db.database import get_db
from app.schemas.services import (
    ServiceCreate,
    ServiceOut,
    ServiceUpdate,
)
from app.dependencies.auth import get_current_user

from app.models.services import Service
from app.services.ServiceService import ServiceService
from app.core.messages import messages
from app.api.owner_router import get_service as get_owner_service
from app.api.salon_router import get_service
from app.schemas.response import ResponseSchema

router = APIRouter(prefix="/services", tags=["Services"])


def get_service_service():
    repo = CRUDBase(Service)
    salon_service = get_service()
    owner_service = get_owner_service()
    return ServiceService(
        repo, salon_service=salon_service, owner_service=owner_service
    )


@router.post(
    "/", response_model=ResponseSchema[ServiceOut], status_code=status.HTTP_201_CREATED
)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    service_service: ServiceService = Depends(get_service_service),
):
    data = service_service.create_service(
        db, service_in, user_role=user["role"], user_id=user["sub"]
    )

    return ResponseSchema(data=data, message=messages.SERVICE_CREATED)


@router.get("/", response_model=ResponseSchema[list[ServiceOut]])
def get_services(
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    data = service_service.get_services(db)

    return ResponseSchema(data=data, message=messages.SERVICES_FOUND)


@router.get("/{service_id}", response_model=ResponseSchema[ServiceOut])
def get_services(
    service_id: int,
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    data = service_service.get_service(db, service_id)

    return ResponseSchema(data=data, message=messages.SERVICE_FOUND)


@router.put("/{service_id}", response_model=ResponseSchema[ServiceOut])
def update_service(
    service_id: int,
    service_in: ServiceUpdate,
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    data = service_service.update_service(db, service_id, service_in)

    return ResponseSchema(data=data, message=messages.SERVICE_UPDATED)


@router.delete("/{service_id}", response_model=ResponseSchema[ServiceOut])
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    data = service_service.delete_service(db, service_id)

    return ResponseSchema(data=data, message=messages.SERVICE_DELETED)
