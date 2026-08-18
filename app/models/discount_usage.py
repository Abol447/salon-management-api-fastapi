from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class DiscountUsage(Base):
    __tablename__ = "discount_usages"

    id = Column(Integer, primary_key=True, index=True)

    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    discount = relationship("Discount", back_populates="usages")

    customer = relationship("Customer", back_populates="discount_usages")

    appointment = relationship("Appointment", back_populates="discount_usage")
