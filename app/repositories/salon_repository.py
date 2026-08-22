from sqlalchemy.orm import Session

from app.schemas.salon import SalonCreate, SalonUpdate, CustomerFilter
from app.models.salon import Salon
from app.models.customer import Customer
from app.models.user import User
from app.models.owner import Owner
from app.repositories.base.CRUDBase import CRUDBase


class SalonRepository(CRUDBase[Salon, SalonCreate, SalonUpdate]):

    def __init__(self):
        super().__init__(Salon)

    def filter_customer(
        self, db: Session, user_id: int, customer_filter: CustomerFilter
    ):
        salon = self.first_by(db, user_id=user_id)

        query = (
            db.query(
                Customer,
                User.first_name.label("first_name"),
                User.last_name.label("last_name"),
                User.phone.label("phone_number"),
            )
            .join(User, User.id == Customer.user_id)
            .filter(Customer.salon_id == salon.id)
        )

        if customer_filter.first_name:
            query = query.filter(
                User.first_name.like(f"%{customer_filter.first_name}%")
            )

        if customer_filter.last_name:
            query = query.filter(User.last_name.like(f"%{customer_filter.last_name}%"))

        if customer_filter.phone:
            query = query.filter(User.phone.like(f"%{customer_filter.phone}%"))

        return query.all()
