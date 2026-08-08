from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.base.CRUDBase import CRUDBase

from app.services.customer_service import CustomerService

from app.schemas.customer import (
    CustomerResponse,
    CustomerUpdate,
    CustomerCreate
)

from app.db.database import get_db
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/customer",
    tags=["customer"]
)


def GetCustomerService():
    repo = CRUDBase(Customer)
    return CustomerService(repo=repo)



@router.post(
    "",
    response_model=CustomerResponse
)
def CreateCustomer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService)
):
    return service.CreateCustomer(
        db=db,
        customer_data=customer_data
    )




@router.get(
    "/me",
    response_model=CustomerResponse
)
def GetMyCustomer(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService)
):
    return service.get_by_user_id(
        db,
        int(user["sub"])
    )



@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def GetCustomer(
    customer_id: int,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService)
):
    return service.get(
        db,
        customer_id
    )




@router.get(
    "",
    response_model=list[CustomerResponse]
)
def GetCustomers(
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService)
):
    return service.get_all(db)


@router.put(
    "",
    response_model=CustomerResponse
)
def UpdateCustomer(
    customer_data: CustomerUpdate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService)
):
    return service.update(
        db,
        customer_data,
        int(user["sub"])
    )



@router.delete(
    "",
    response_model=CustomerResponse
)
def DeleteCustomer(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: CustomerService = Depends(GetCustomerService)
):
    return service.delete(
        db,
        int(user["sub"])
    )