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
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class WalletTransactionService:

    def __init__(
        self,
        repo: CRUDBase[WalletTransaction, WalletTransactionCreate],
        wallet_repo: CRUDBase[Wallet, WalletCreate, WalletUpdate],
        customer_repo: CRUDBase[Customer, CustomerCreate, CustomerUpdate],
    ):
        self.repo = repo
        self.wallet_repo = wallet_repo
        self.customer_repo = customer_repo

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

    def get_by_id(self, db: Session, id: int, role: str):
        try:
            if role.lower() == "customer":
                customer = self.customer_repo.first_by(db, user_id=id)
                wallet = self.wallet_repo.first_by(db, customer_id=customer.id)
                transaction = self.repo.filter_by(db, wallet_id=wallet.id)
                logger.info(f"get transaction by customer id : {id}")
                return transaction

        except Exception as e:
            print(e)
            logger.error(f"failed to get customer transaction")
            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)
