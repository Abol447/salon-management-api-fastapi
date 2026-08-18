from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Discount(Base):
    __tablename__ = "discounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"), nullable=False
    )

    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    max_usage: Mapped[int | None] = mapped_column(Integer, default=1)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    customer = relationship("Customer", back_populates="discount")

    usages = relationship("DiscountUsage", back_populates="discount")
