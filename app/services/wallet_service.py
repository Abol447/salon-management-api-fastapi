from app.repositories.base.CRUDBase import CRUDBase
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate, WalletUpdate
from app.exceptions import NotFoundException, InternalServerException
from app.core.logger import logger
from app.core.messages import messages
from sqlalchemy.orm import Session


class WalletService:

    def __init__(self, repo: CRUDBase[Wallet, WalletCreate, WalletUpdate]):
        self.repo = repo

    def create(self, db: Session, data_in: WalletCreate, auto_commit: bool = True):
        try:
            wallet = self.repo.create(db, data_in, auto_commit=auto_commit)

            logger.info(
                f"wallet created successfully for customer id={data_in.customer_id}"
            )

            return wallet

        except Exception as e:
            logger.error(
                f"failed to create wallet for customer " f"{data_in.customer_id}: {e}"
            )

            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)

    def get_by_id(self, db: Session, wallet_id: int):
        try:
            wallet = self.repo.get_by_id(db, wallet_id)

            if not wallet:
                raise NotFoundException(messages.WALLET_NOT_FOUND)

            return wallet

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to get wallet id={wallet_id}: {e}")

            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)

    def get_by_customer_id(self, db: Session, customer_id: int):
        try:
            wallets = self.repo.filter_by(db, customer_id=customer_id)

            if not wallets:
                raise NotFoundException(messages.WALLET_NOT_FOUND)

            return wallets[0]

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to get wallet for customer " f"id={customer_id}: {e}")

            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)

    def update(
        self,
        db: Session,
        wallet_id: int,
        data_in: WalletUpdate,
        auto_commit: bool = True,
    ):
        try:
            wallet = self.repo.get_by_id(db, wallet_id)

            if not wallet:
                raise NotFoundException(messages.WALLET_NOT_FOUND)

            wallet = self.repo.update(db, wallet, data_in, auto_commit=auto_commit)

            logger.info(f"wallet updated successfully id={wallet_id}")

            return wallet

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to update wallet id={wallet_id}: {e}")

            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)

    def delete(self, db: Session, wallet_id: int):
        try:
            wallet = self.repo.get_by_id(db, wallet_id)

            if not wallet:
                raise NotFoundException(messages.WALLET_NOT_FOUND)

            result = self.repo.delete(db, wallet)

            logger.info(f"wallet deleted successfully id={wallet_id}")

            return result

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to delete wallet id={wallet_id}: {e}")

            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)
