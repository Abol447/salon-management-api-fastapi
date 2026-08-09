from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.base.CRUDBase import CRUDBase
from app.db.database import get_db
from app.schemas.services import (
    ServiceCreate,
    ServiceOut,
    ServiceUpdate,
)

from app.models.services import Service
from app.services.ServiceService import ServiceService

router = APIRouter(prefix="/services", tags=["Services"])


def get_service_service():
    repo = CRUDBase(Service)
    return ServiceService(repo)


@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    return service_service.create_service(db, service_in)


@router.get("/", response_model=list[ServiceOut])
def get_services(
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    return service_service.get_services(db)


@router.get("/{service_id}", response_model=ServiceOut)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    service = service_service.get_service(db, service_id)
    return service


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    service_in: ServiceUpdate,
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    service = service_service.update_service(db, service_id, service_in)

    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    service_service: ServiceService = Depends(get_service_service),
):
    service = service_service.delete_service(db, service_id)
    return None
