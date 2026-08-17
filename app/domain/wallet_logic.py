from decimal import Decimal
from fastapi import HTTPException

from app.enums.wallet_transaction import WalletTranceactionType
from app.models.wallet import Wallet
from app.schemas.wallet import WalletUpdate
from app.exceptions import BadRequestException, InternalServerException
from app.core.logger import logger
from app.core.messages import messages


def wallet_balance(
    wallet: Wallet, type: WalletTranceactionType, amount: Decimal
) -> tuple[Decimal, Decimal]:
    try:
        balance = wallet.balance
        if type == WalletTranceactionType.CASHBACK:
            balance = balance + amount
            return balance, amount
        else:
            wallet_balence = balance - amount
            if wallet_balence < 0:
                amount = balance
                balance = 0
                return balance, amount
            return wallet_balence, amount

    except Exception as e:
        logger.error(f"internal server error =>{e}")
        raise InternalServerException(messages.INTERNAL_SERVER_ERROR)
