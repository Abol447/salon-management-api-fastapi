from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Numeric , Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.mixins import TimestampMixin, SoftDeleteMixin


class Appointment(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    start_time = Column(DateTime, nullable=False)

    description = Column(Text, nullable=True)

    salon_id = Column(Integer, ForeignKey("salons.id"), nullable=False)

    is_paid = Column(Boolean , default= False)

    paid_price = Column(Numeric(10, 2), nullable=True)

    wallet_transactions = relationship(
        "WalletTransaction", back_populates="appointment"
    )

    customer = relationship("Customer", back_populates="appointments")

    salon = relationship("Salon", back_populates="appointment")

    discount_usage = relationship(
        "DiscountUsage", back_populates="appointment", uselist=False
    )

    appointment_services = relationship(
        "AppointmentService", back_populates="appointment", cascade="all, delete-orphan"
    )
