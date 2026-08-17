from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.AppointmentService import AppointmentService
from app.schemas.AppointmentService import (
    AppointmentServiceResponse,
    AppointmentServiceCreate,
    AppointmentServiceUpdate,
)
from app.repositories.base.CRUDBase import CRUDBase
from app.services.appoinmtmentService_service import AppointmentService_service
from app.db.database import get_db
from app.schemas.response import ResponseSchema
from app.core.messages import messages

router = APIRouter(
    prefix="/appointment_service",
    tags=["appointment_service"],
)


def get_service():
    repo = CRUDBase(AppointmentService)
    return AppointmentService_service(repo)


@router.post(
    "",
    response_model=ResponseSchema[AppointmentServiceResponse],
)
def create(
    data_in: AppointmentServiceCreate,
    db: Session = Depends(get_db),
    service: AppointmentService_service = Depends(get_service),
):
    data = service.create(db, data_in)

    return ResponseSchema(
        data=data,
        message=messages.CREATED,
    )


@router.get(
    "",
    response_model=ResponseSchema[list[AppointmentServiceResponse]],
)
def get_all(
    db: Session = Depends(get_db),
    service: AppointmentService_service = Depends(get_service),
):
    data = service.get_all(db)

    return ResponseSchema(
        data=data,
        message=messages.GET_ALL,
    )


@router.get(
    "/{appointment_service_id}",
    response_model=ResponseSchema[AppointmentServiceResponse],
)
def get(
    appointment_service_id: int,
    db: Session = Depends(get_db),
    service: AppointmentService_service = Depends(get_service),
):
    data = service.get(
        db,
        appointment_service_id,
    )

    return ResponseSchema(
        data=data,
        message=messages.GET_ALL,
    )


@router.put(
    "/{appointment_service_id}",
    response_model=ResponseSchema[AppointmentServiceResponse],
)
def update(
    appointment_service_id: int,
    data_in: AppointmentServiceUpdate,
    db: Session = Depends(get_db),
    service: AppointmentService_service = Depends(get_service),
):
    data = service.update(
        db,
        appointment_service_id,
        data_in,
    )

    return ResponseSchema(
        data=data,
        message=messages.UPDATED,
    )


@router.delete(
    "/{appointment_service_id}",
    response_model=ResponseSchema[AppointmentServiceResponse],
)
def delete(
    appointment_service_id: int,
    db: Session = Depends(get_db),
    service: AppointmentService_service = Depends(get_service),
):
    data = service.delete(
        db,
        appointment_service_id,
    )

    return ResponseSchema(
        data=data,
        message=messages.DELETED,
    )
