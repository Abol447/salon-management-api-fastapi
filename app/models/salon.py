from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, SoftDeleteMixin


class Salon(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "salons"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    location = Column(Text, nullable=False)

    back_percent = Column(DECIMAL(3, 1), default=DECIMAL("10"))

    customer = relationship("Customer", back_populates="salon")

    appointment = relationship("Appointment", back_populates="salon")

    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)

    service = relationship("Service", back_populates="salon")

    owner = relationship("Owner", back_populates="salons")
