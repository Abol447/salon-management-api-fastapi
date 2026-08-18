from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.repositories.base.CRUDBase import CRUDBase
from app.models.discount import Discount
from app.schemas.discount import DiscountCreate, DiscountUpdate
from app.models.discount_usage import DiscountUsage


class DiscountRepo(CRUDBase[Discount, DiscountCreate, DiscountUpdate]):

    def __init__(self):
        super().__init__(Discount)

    def get_my_discount(self, db: Session, customer_id: int):
        query = (
            db.query(Discount, func.count(DiscountUsage.id).label("usage_count"))
            .outerjoin(
                DiscountUsage,
                (Discount.id == DiscountUsage.discount_id)
                & (DiscountUsage.customer_id == customer_id),
            )
            .filter(
                Discount.is_active == True,
                Discount.end_date > datetime.now(),
                Discount.customer_id == customer_id,
            )
            .group_by(Discount.id)
            .all()
        )
        data = []
        for item in query:
            if item.usage_count < item.Discount.max_usage:
                data.append(
                    {"discount": item.Discount, "discount_usage": item.usage_count}
                )

        return data
