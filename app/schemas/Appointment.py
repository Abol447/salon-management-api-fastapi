from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.schemas.AppointmentService import AppointmentServiceResponse


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
    service_id: list[int]
    start_time: datetime
    description: str | None = None
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
    UpdatedAt: datetime
    salon_id: int
    IsDeleted: bool

    model_config = ConfigDict(from_attributes=True)
