from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.base.CRUDBase import CRUDBase
from app.services.customer_service import CustomerService
from app.schemas.customer import CustomerResponse, CustomerUpdate, CustomerCreate
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.core.messages import messages
from app.schemas.response import ResponseSchema

router = APIRouter(prefix="/customer", tags=["customer"])


def GetCustomerService():
    repo = CRUDBase(Customer)
    return CustomerService(repo=repo)


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

    return ResponseSchema(data=data, message=messages.CUSTOMER_FOUND)


@router.get("/{customer_id}", response_model=ResponseSchema[CustomerResponse])
def GetCustomer(
    customer_id: int,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService),
):
    data = service.get(db, customer_id)

    return ResponseSchema(data=data, message=messages.CUSTOMER_FOUND)


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
