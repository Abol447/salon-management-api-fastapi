from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.schemas.customer import CustomerResponse


class SalonCreate(BaseModel):
    name: str
    location: str
    back_percent: Decimal
    owner_id: int


class SalonUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    back_percent: Decimal | None = None


class SalonResponse(BaseModel):
    id: int
    name: str
    location: str
    owner_id: int
    back_percent: Decimal

    model_config = ConfigDict(from_attributes=True)


class CustomerFilterOut(BaseModel):
    customer: CustomerResponse
    first_name: str | None = None
    last_name: str | None = None
    phone: str

    model_config = ConfigDict(from_attributes=True)


class CustomerFilter(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
