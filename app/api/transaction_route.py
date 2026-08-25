from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.wallet_transaction import WalletTransaction
from app.models.wallet import Wallet
from app.models.customer import Customer
from app.db.database import get_db
from app.schemas.wallet_transaction import WalletTransactionCreate, WalletTransactionOut
from app.services.wallet_transaction_service import WalletTransactionService
from app.repositories.base.CRUDBase import CRUDBase
from app.models.wallet_transaction import WalletTransaction
from app.dependencies.auth import require_roles
from app.schemas.response import ResponseSchema
from app.core.messages import messages

router = APIRouter(prefix="/wallet-transactions", tags=["Wallet Transactions"])


def get_wallet_transaction_service():
    repo = CRUDBase(WalletTransaction)
    wallet_repo = CRUDBase(Wallet)
    transaction = CRUDBase(Customer)
    return WalletTransactionService(repo, wallet_repo, transaction)


@router.post(
    "/",
    response_model=ResponseSchema[WalletTransactionOut],
    status_code=status.HTTP_201_CREATED,
)
def create_wallet_transaction(
    data: WalletTransactionCreate,
    db: Session = Depends(get_db),
    service: WalletTransactionService = Depends(get_wallet_transaction_service),
):
    return ResponseSchema(data=service.create(db, data), message=messages.GET_ALL)


@router.get("/customer", response_model=ResponseSchema[list[WalletTransactionOut]])
def get_transaction(
    db: Session = Depends(get_db),
    service: WalletTransactionService = Depends(get_wallet_transaction_service),
    user: dict = Depends(require_roles("customer")),
):
    return ResponseSchema(
        data=service.get_by_id(db, user["sub"], user["role"]), message=messages.GET_ALL
    )
