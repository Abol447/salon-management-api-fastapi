from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class WalletCreate(BaseModel):
    customer_id: int
    balance: Decimal = Decimal("0")


class WalletUpdate(BaseModel):
    balance: Decimal | None = None


class WalletOut(BaseModel):
    id: int
    customer_id: int
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)
