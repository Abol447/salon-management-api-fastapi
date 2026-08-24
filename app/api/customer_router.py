from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.Appointment import AppointmentOut
from app.services.customer_service import CustomerService
from app.schemas.customer import (
    CustomerResponse,
    CustomerUpdate,
    CustomerCreate,
    GetCustomerAppointment,
)
from app.dependencies.auth import require_roles
from app.api.appointment_router import get_appointment_service
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.core.messages import messages
from app.schemas.response import ResponseSchema
from app.models.appointment import Appointment
from app.api.salon_router import get_service
from app.api.owner_router import get_service as get_owner_service

router = APIRouter(prefix="/customer", tags=["customer"])


def GetCustomerService():
    repo = CRUDBase(Customer)
    appointment_repo = CRUDBase(Appointment)
    salon_service = get_service()
    owner_service = get_owner_service()

    return CustomerService(
        repo=repo,
        appointment_repo=appointment_repo,
        salon_service=salon_service,
        owner_service=owner_service,
    )


@router.post("", response_model=ResponseSchema[CustomerResponse])
def CreateCustomer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService),
):
    data = service.CreateCustomer(db=db, customer_data=customer_data)

    return ResponseSchema(data=data, message=messages.CUSTOMER_CREATED)


@router.get("/me", response_model=ResponseSchema[CustomerResponse])
def GetMyCustomer(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService),
):
    data = service.get_by_user_id(db, int(user["sub"]))

    return ResponseSchema(data=data, message=messages.GET_ALL)


@router.get("/appointments", response_model=list[AppointmentOut])
def get_customer_appointments(
    data_in: GetCustomerAppointment = Depends(),
    db: Session = Depends(get_db),
    user: dict = Depends(require_roles("owner")),
    service: CustomerService = Depends(GetCustomerService),
):
    return service.get_appointment(db=db, data_in=data_in, owner_id=user["sub"])


@router.get("/{customer_id}", response_model=ResponseSchema[CustomerResponse])
def GetCustomer(
    customer_id: int,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService),
):
    data = service.get(db, customer_id)

    return ResponseSchema(data=data, message=messages.GET_ALL)


@router.get("", response_model=ResponseSchema[list[CustomerResponse]])
def GetCustomers(
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService),
):
    data = service.get_all(db)

    return ResponseSchema(data=data, message=messages.CUSTOMERS_FOUND)


@router.put("", response_model=ResponseSchema[CustomerResponse])
def UpdateCustomer(
    customer_data: CustomerUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService),
):
    data = service.update(db, customer_data, int(user["sub"]))

    return ResponseSchema(data=data, message=messages.CUSTOMER_UPDATED)


@router.delete("", response_model=ResponseSchema[CustomerResponse])
def DeleteCustomer(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService),
):
    data = service.delete(db, int(user["sub"]))

    return ResponseSchema(data=data, message=messages.CUSTOMER_DELETED)
