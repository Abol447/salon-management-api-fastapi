from sqlalchemy import Column, Integer, DateTime, Text, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base
from app.db.mixins import TimestampMixin, SoftDeleteMixin


class Appointment(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    start_time = Column(DateTime, nullable=False)

    description = Column(Text, nullable=True)

    paid_price = Column(Numeric(10, 2), nullable=True)

    customer = relationship("Customer", back_populates="appointments")

    service = relationship("Service", back_populates="appointments")
