from decimal import Decimal
from sqlalchemy.orm import Session

from app.schemas.customer import CustomerCreate
from app.schemas.wallet import WalletCreate
from app.schemas.discount import DiscountCreate


def create_customer(
    customer_service,
    wallet_service,
    user,
    discount_service,
    salon_id,
    db: Session,
):
    customer = customer_service.create(
        db,
        CustomerCreate(user_id=user.id, salon_id=salon_id),
        auto_commit=False,
    )
    wallet = wallet_service.create(
        db, WalletCreate(customer_id=customer.id), auto_commit=False
    )
    discount = discount_service.create(
        db,
        DiscountCreate(
            customer_id=customer.id,
            max_usage=1,
            is_active=True,
            percent=Decimal("10"),
            title="welcom",
        ),
    )
    db.flush()
    return customer, wallet, discount
