from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, SoftDeleteMixin


class Salon(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "salons"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    location = Column(Text, nullable=False)

    appointment = relationship("Appointment", back_populates="salon")

    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)

    owner = relationship("Owner", back_populates="salons")
