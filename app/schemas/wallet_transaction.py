from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.enums.wallet_transaction import WalletTranceactionType


class WalletTransactionCreate(BaseModel):
    wallet_id: int
    appointment_id: int | None = None
    amount: Decimal
    type: WalletTranceactionType
    description: str | None = None


class WalletTransactionUpdate(BaseModel):
    wallet_id: int | None = None
    appointment_id: int | None = None
    amount: Decimal | None = None
    type: WalletTranceactionType | None = None
    description: str | None = None


class WalletTransactionOut(BaseModel):
    id: int
    wallet_id: int
    appointment_id: int | None = None
    amount: Decimal
    type: WalletTranceactionType
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
