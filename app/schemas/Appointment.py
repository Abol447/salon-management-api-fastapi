from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    phone_number: str
    service_id: int
    start_time: datetime
    description: str | None = None
    paid_price: Decimal | None = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentCreateInternal(BaseModel):
    customer_id: int
    service_id: int
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
    service_id: int
    start_time: datetime
    description: str | None
    paid_price: Decimal | None

    CreatedAt: datetime
    UpdatedAt: datetime
    IsDeleted: bool

    model_config = ConfigDict(from_attributes=True)
