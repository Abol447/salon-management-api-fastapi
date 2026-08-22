from sqlalchemy import Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    birthday: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    profile_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True, index=True
    )

    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id"), nullable=True, index=True
    )

    wallet = relationship("Wallet", back_populates="customer")

    appointments = relationship("Appointment", back_populates="customer")

    discount = relationship("Discount", back_populates="customer")

    user = relationship("User", back_populates="customer")

    salon = relationship("Salon", back_populates="customer")

    discount_usages = relationship("DiscountUsage", back_populates="customer")
