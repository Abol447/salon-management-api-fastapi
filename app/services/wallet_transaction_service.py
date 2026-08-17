from app.models.wallet_transaction import WalletTransaction
from app.schemas.wallet_transaction import (
    WalletTransactionOut,
    WalletTransactionCreate,
    WalletTransactionUpdate,
)
from app.repositories.base.CRUDBase import CRUDBase
from app.enums.wallet_transaction import WalletTranceactionType
from app.exceptions import (
    InternalServerException,
    NotFoundException,
    BadRequestException,
)
from app.core.logger import logger
from app.core.messages import messages
from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate, WalletUpdate
from decimal import Decimal
from app.domain.wallet_logic import wallet_balance
from fastapi import HTTPException


class WalletTransactionService:

    def __init__(
        self,
        repo: CRUDBase[WalletTransaction, WalletTransactionCreate],
        wallet_repo: CRUDBase[Wallet, WalletCreate, WalletUpdate],
    ):
        self.repo = repo
        self.wallet_repo = wallet_repo

    def create(self, db: Session, data_in: WalletTransactionCreate):
        try:
            wallet = self.wallet_repo.get_by_id(db, data_in.wallet_id)

            if wallet is None:
                raise BadRequestException("کیف پول یافت نشد ")

            balance, amount = wallet_balance(wallet, data_in.type, data_in.amount)

            if amount == 0:
                raise BadRequestException("موجودی کافیی نمی باشد ")

            self.wallet_repo.update(
                db, wallet, WalletUpdate(balance=balance), auto_commit=False
            )

            data_in.amount = amount

            transaction = self.repo.create(db, data_in, auto_commit=False)

            db.commit()
            db.refresh(transaction)

            return transaction

        except HTTPException:
            raise

        except Exception:
            db.rollback()
            raise
