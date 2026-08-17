from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0)
