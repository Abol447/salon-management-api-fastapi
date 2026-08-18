from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class DiscountCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)

    percent: Decimal = Field(ge=0, le=100)

    start_date: datetime

    end_date: datetime

    max_usage: int = Field(default=1, ge=1)

    is_active: bool = True


class MyDiscount(BaseModel):
    discount: DiscountResponse
    discount_usage: int


class DiscountUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)

    percent: Decimal | None = Field(default=None, ge=0, le=100)

    start_date: datetime | None = None

    end_date: datetime | None = None

    max_usage: int | None = Field(default=None, ge=1)

    is_active: bool | None = None


class DiscountResponse(BaseModel):
    id: int
    title: str
    percent: Decimal
    start_date: datetime
    end_date: datetime
    max_usage: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
