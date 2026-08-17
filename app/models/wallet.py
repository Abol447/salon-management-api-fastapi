from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer, ForeignKey("customers.id"), unique=True, nullable=False
    )

    balance = Column(Numeric(12, 2), nullable=False, default=0)
    transactions = relationship("WalletTransaction", back_populates="wallet")
    customer = relationship("Customer", back_populates="wallet")
