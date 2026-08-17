from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.repositories.base.CRUDBase import CRUDBase
from app.models.wallet import Wallet
from app.db.database import get_db
from app.schemas.wallet import WalletCreate, WalletOut, WalletUpdate
from app.services.wallet_service import WalletService

router = APIRouter(prefix="/wallets", tags=["Wallet"])


def get_wallet_service():
    repo = CRUDBase(Wallet)
    return WalletService(repo)


@router.post("/", response_model=WalletOut)
def create_wallet(
    data: WalletCreate,
    db: Session = Depends(get_db),
    service: WalletService = Depends(get_wallet_service),
):
    return service.create(db, data)


@router.get("/{wallet_id}", response_model=WalletOut)
def get_wallet(
    wallet_id: int,
    db: Session = Depends(get_db),
    service: WalletService = Depends(get_wallet_service),
):
    return service.get_by_id(db, wallet_id)


@router.get("/customer/{customer_id}", response_model=WalletOut)
def get_customer_wallet(
    customer_id: int,
    db: Session = Depends(get_db),
    service: WalletService = Depends(get_wallet_service),
):
    return service.get_by_customer_id(db, customer_id)


@router.put("/{wallet_id}", response_model=WalletOut)
def update_wallet(
    wallet_id: int,
    data: WalletUpdate,
    db: Session = Depends(get_db),
    service: WalletService = Depends(get_wallet_service),
):
    return service.update(db, wallet_id, data)


@router.delete("/{wallet_id}", response_model=WalletOut)
def delete_wallet(
    wallet_id: int,
    db: Session = Depends(get_db),
    service: WalletService = Depends(get_wallet_service),
):
    return service.delete(db, wallet_id)
