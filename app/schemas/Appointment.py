from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.schemas.AppointmentService import AppointmentServiceResponse
from datetime import date
from pydantic import BaseModel
from decimal import Decimal
from app.schemas.customer import CustomerResponse


class AppointmentBase(BaseModel):
    phone_number: str
    service_id: list[int]
    start_time: datetime
    description: str | None = None
    salon_id: int
    paid_price: Decimal | None = None


class AppointmentCreate(AppointmentBase):
    pass


class PayPrice(BaseModel):
    pay_price: Decimal 
    appointment_id: int
    customer_id: int


class AppointmentCreateInternal(BaseModel):
    customer_id: int
    start_time: datetime
    description: str | None = None
    salon_id: int
    paid_price: Decimal | None = None


class AppointmentUpdate(BaseModel):
    start_time: datetime | None = None
    description: str | None = None
    paid_price: Decimal | None = None


class AppointmentOut(BaseModel):
    id: int
    customer_id: int
    appointment_services: list[AppointmentServiceResponse]
    start_time: datetime
    description: str | None
    paid_price: Decimal | None
    CreatedAt: datetime
    customer: CustomerResponse
    UpdatedAt: datetime
    salon_id: int
    is_paid : bool
    IsDeleted: bool

    model_config = ConfigDict(from_attributes=True)


class AppointmentFilter(BaseModel):
    customer_id: int | None = None
    salon_id: int | None = None
    service_id: int | None = None
    phone: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    paid: bool | None = None

    page: int = 1
    page_size: int = 10


class AppointmentFilterOut(BaseModel):
    appointment: list[AppointmentOut]
    page_size: int
    total: int
    page: int
    total_page: int
