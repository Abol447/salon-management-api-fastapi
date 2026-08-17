from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.wallet_transaction import WalletTransaction
from app.models.wallet import Wallet
from app.db.database import get_db
from app.schemas.wallet_transaction import WalletTransactionCreate, WalletTransactionOut
from app.services.wallet_transaction_service import WalletTransactionService
from app.repositories.base.CRUDBase import CRUDBase

router = APIRouter(prefix="/wallet-transactions", tags=["Wallet Transactions"])


def get_wallet_transaction_service():
    repo = CRUDBase(WalletTransaction)
    wallet_repo = CRUDBase(Wallet)
    return WalletTransactionService(repo, wallet_repo)


@router.post(
    "/", response_model=WalletTransactionOut, status_code=status.HTTP_201_CREATED
)
def create_wallet_transaction(
    data: WalletTransactionCreate,
    db: Session = Depends(get_db),
    service: WalletTransactionService = Depends(get_wallet_transaction_service),
):
    return service.create(db, data)
