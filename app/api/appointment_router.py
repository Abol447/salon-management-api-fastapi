from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.Appointment import (
    AppointmentCreate,
    PayPrice,
    AppointmentUpdate,
    AppointmentOut,
)
from app.models.owner import Owner
from app.dependencies.auth import require_roles, get_current_user
from app.services.appointment_service import AppointmentService

from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.base.CRUDBase import CRUDBase
from app.services.wallet_service import WalletService
from app.services.wallet_transaction_service import WalletTransactionService
from app.models.customer import Customer
from app.models.discount import Discount
from app.models.user import User
from app.models.role import Role
from app.core.messages import messages
from app.schemas.response import ResponseSchema
from app.api.wallet_router import get_wallet_service
from app.api.transaction_route import get_wallet_transaction_service
from app.api.user_route import get_user_service
from app.api.appointmentService_router import get_service

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def get_appointment_service() -> AppointmentService:
    repo = AppointmentRepository()

    discount_repo = CRUDBase(Discount)
    user_repo = get_user_service()
    role_repo = CRUDBase(Role)
    customer_repo = CRUDBase(Customer)
    owner_repo = CRUDBase(Owner)
    transaction = get_wallet_transaction_service()
    wallet = get_wallet_service()
    aappointment_service = get_service()
    return AppointmentService(
        repo,
        discount_repo,
        user_repo,
        role_repo,
        customer_repo,
        owner_repo,
        transaction,
        wallet,
        aappointment_service,
    )


@router.post("/", response_model=ResponseSchema[AppointmentOut], status_code=201)
def create_appointment(
    appointment_data: AppointmentCreate,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    data = service.create(db, appointment_data)

    return ResponseSchema(data=data, message=messages.APPOINTMENT_CREATED)


@router.get("/", response_model=ResponseSchema[list[AppointmentOut]])
def get_appointments(
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    data = service.get_all(db)
    return ResponseSchema(data=data, message="نوبت ها با موفقیت دریافت شد ")


@router.get("/me", response_model=ResponseSchema[list[AppointmentOut]])
def get_appointments(
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    appointment = service.get_customer_appointment(db, user["sub"], user["role"])
    return ResponseSchema(data=appointment, message=messages.GET_ALL)


@router.get("/{appointment_id}", response_model=ResponseSchema[AppointmentOut])
def get_appointment(
    appointment_id: int,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    data = service.get_by_id(db, appointment_id)

    return ResponseSchema(data=data, message=messages.APPOINTMENT_FOUND)


@router.put("/{appointment_id}", response_model=ResponseSchema[AppointmentOut])
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    data = service.update(db, appointment_id, appointment_data)

    return ResponseSchema(data=data, message=messages.APPOINTMENT_UPDATED)


@router.delete("/{appointment_id}", response_model=ResponseSchema[AppointmentOut])
def delete_appointment(
    appointment_id: int,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    data = service.delete(db, appointment_id)

    return ResponseSchema(data=data, message=messages.APPOINTMENT_DELETED)


@router.post("/pay", response_model=ResponseSchema[AppointmentOut])
def pay(
    data_in: PayPrice,
    service: AppointmentService = Depends(get_appointment_service),
    db: Session = Depends(get_db),
):
    data = service.pay(db, data_in)
    return ResponseSchema(data=data, message=messages.SUCCESS)
