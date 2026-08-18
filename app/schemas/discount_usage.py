from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.discount import DiscountResponse


class DiscountUsageCreate(BaseModel):
    discount_id: int
    customer_id: int
    appointment_id: int


class DiscountUsageUpdate(BaseModel):
    discount_id: int | None = None
    customer_id: int | None = None
    appointment_id: int | None = None


class DiscountUsageOut(BaseModel):
    id: int
    discount_id: int
    customer_id: int
    appointment_id: int
    discount: DiscountResponse
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
