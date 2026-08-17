from sqlalchemy import Column, Enum, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.enums.wallet_transaction import WalletTranceactionType
from app.db.base import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)

    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)

    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)

    amount = Column(Numeric(12, 2), nullable=False)

    type = Column(Enum(WalletTranceactionType), nullable=False)

    description = Column(String(255), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    wallet = relationship("Wallet", back_populates="transactions")

    appointment = relationship("Appointment", back_populates="wallet_transactions")
