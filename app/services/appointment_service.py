import secrets

from sqlalchemy.orm import Session

from app.repositories.appointment_repository import (
    AppointmentRepository,
    AppointmentCreate,
    AppointmentUpdate,
    CRUDBase,
)

from app.core.security import hash_password
from app.core.logger import logger
from app.exceptions import InternalServerException

from app.schemas.Appointment import AppointmentCreateInternal
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.schemas.discount import DiscountCreate, DiscountUpdate
from app.schemas.user import UserCreate, UserUpdate, SystemUserCreate
from app.schemas.role import RoleCreate, RoleUpdate

from app.models.appointment import Appointment
from app.models.customer import Customer
from app.models.discount import Discount
from app.models.user import User
from app.models.role import Role


class AppointmentService:

    def __init__(
        self,
        repo: AppointmentRepository,
        discount_repo: CRUDBase[Discount, DiscountCreate, DiscountUpdate],
        user_repo: CRUDBase[User, UserCreate, UserUpdate],
        role_repo: CRUDBase[Role, RoleCreate, RoleUpdate],
        customer_repo: CRUDBase[Customer, CustomerCreate, CustomerUpdate],
    ):
        self.repo = repo
        self.discount_repo = discount_repo
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.customer_repo = customer_repo

    def create(self, db: Session, appointment_data: AppointmentCreate):
        try:

            user = self.user_repo.first_by(db, phone=appointment_data.phone_number)

            if user is None:

                customer_role = self.role_repo.first_by(db, name="customer")

                if customer_role is None:
                    raise InternalServerException("customer role not found")

                random_password = secrets.token_urlsafe(12)

                user = self.user_repo.create(
                    db,
                    obj_in=SystemUserCreate(
                        phone=appointment_data.phone_number,
                        password_hash=hash_password(random_password),
                        role_id=customer_role.id,
                    ),
                )

                customer = self.customer_repo.create(
                    db, obj_in=CustomerCreate(user_id=user.id)
                )

            else:

                customer = self.customer_repo.first_by(db, user_id=user.id)

                if customer is None:
                    customer = self.customer_repo.create(
                        db, obj_in=CustomerCreate(user_id=user.id)
                    )

            appointment = self.repo.create(
                db,
                obj_in=AppointmentCreateInternal(
                    customer_id=customer.id,
                    service_id=appointment_data.service_id,
                    description=appointment_data.description,
                    start_time=appointment_data.start_time,
                    paid_price=appointment_data.paid_price,
                ),
            )

            return appointment

        except InternalServerException:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()

            logger.exception("Failed to create appointment")

            raise InternalServerException("Failed to create appointment")

    def get_all(self, db: Session):

        try:
            return self.repo.get_all(db)

        except Exception as e:

            logger.exception("Failed to get all appointments")

            raise InternalServerException("Failed to get all appointments")

    def get_by_id(self, db: Session, appointment_id: int):

        try:

            appointment = self.repo.get_by_id(db, appointment_id)

            if appointment is None:
                raise InternalServerException("Appointment not found")

            return appointment

        except InternalServerException:
            raise

        except Exception as e:

            logger.exception(f"Failed to get appointment {appointment_id}")

            raise InternalServerException("Failed to get appointment")

    def update(
        self, db: Session, appointment_id: int, appointment_data: AppointmentUpdate
    ):

        try:

            appointment = self.repo.get_by_id(db, appointment_id)

            if appointment is None:
                raise InternalServerException("Appointment not found")

            appointment = self.repo.update(
                db, db_obj=appointment, obj_in=appointment_data
            )

            return appointment

        except InternalServerException:
            db.rollback()
            raise

        except Exception as e:

            db.rollback()

            logger.exception(f"Failed to update appointment {appointment_id}")

            raise InternalServerException("Failed to update appointment")

    def delete(self, db: Session, appointment_id: int):

        try:

            appointment = self.repo.get_by_id(db, appointment_id)

            if appointment is None:
                raise InternalServerException("Appointment not found")

            return self.repo.delete(db, id=appointment_id)

        except InternalServerException:
            db.rollback()
            raise

        except Exception as e:

            db.rollback()

            logger.exception(f"Failed to delete appointment {appointment_id}")

            raise InternalServerException("Failed to delete appointment")
