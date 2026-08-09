from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.Appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentOut,
)

from app.services.appointment_service import AppointmentService

from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.base.CRUDBase import CRUDBase

from app.models.customer import Customer
from app.models.discount import Discount
from app.models.user import User
from app.models.role import Role

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def get_appointment_service() -> AppointmentService:
    repo = AppointmentRepository()

    discount_repo = CRUDBase(Discount)
    user_repo = CRUDBase(User)
    role_repo = CRUDBase(Role)
    customer_repo = CRUDBase(Customer)

    return AppointmentService(repo, discount_repo, user_repo, role_repo, customer_repo)


@router.post("/", response_model=AppointmentOut, status_code=201)
def create_appointment(
    appointment_data: AppointmentCreate,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    return service.create(db, appointment_data)


@router.get("/", response_model=list[AppointmentOut])
def get_appointments(
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    return service.get_all(db)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(
    appointment_id: int,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    return service.get_by_id(db, appointment_id)


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    return service.update(db, appointment_id, appointment_data)


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(
    appointment_id: int,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    service.delete(db, appointment_id)
