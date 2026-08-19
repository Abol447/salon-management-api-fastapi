from decimal import Decimal
import secrets

from sqlalchemy.orm import Session

from app.repositories.appointment_repository import (
    AppointmentRepository,
    AppointmentCreate,
    AppointmentUpdate,
    CRUDBase,
)
from app.core.messages import messages
from app.core.security import hash_password
from app.core.logger import logger
from app.exceptions import InternalServerException, NotFoundException
from fastapi import HTTPException
from app.schemas.Appointment import AppointmentCreateInternal, PayPrice
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.schemas.discount import DiscountCreate, DiscountUpdate
from app.schemas.user import UserCreate, UserUpdate, SystemUserCreate
from app.schemas.role import RoleCreate, RoleUpdate
from app.models.owner import Owner
from app.schemas.wallet_transaction import (
    WalletTransactionCreate,
    WalletTranceactionType,
)
from app.schemas.owner import OwnerUpdate, OwnerCreate
from app.models.appointment import Appointment
from app.models.customer import Customer
from app.models.discount import Discount
from app.services.wallet_transaction_service import WalletTransactionService
from app.models.user import User
from app.models.role import Role
from app.services.wallet_service import WalletService
from app.services.user_service import UserService, UserCreate
from app.services.appoinmtmentService_service import (
    AppointmentService_service,
    AppointmentServiceCreate,
)


class AppointmentService:

    def __init__(
        self,
        repo: AppointmentRepository,
        discount_repo: CRUDBase[Discount, DiscountCreate, DiscountUpdate],
        user_service: UserService,
        role_repo: CRUDBase[Role, RoleCreate, RoleUpdate],
        customer_repo: CRUDBase[Customer, CustomerCreate, CustomerUpdate],
        owner_repo: CRUDBase[Owner, OwnerCreate, OwnerUpdate],
        transaction: WalletTransactionService,
        wallet: WalletService,
        appintment_service: AppointmentService_service,
    ):
        self.repo = repo
        self.discount_repo = discount_repo
        self.user_service = user_service
        self.role_repo = role_repo
        self.customer_repo = customer_repo
        self.owner_repo = owner_repo
        self.transaction = transaction
        self.wallet = wallet
        self.appintment_service = appintment_service

    def create(self, db: Session, appointment_data: AppointmentCreate):
        try:

            user = self.user_service.first_users(
                db, phone=appointment_data.phone_number
            )

            if user is None:

                random_password = secrets.token_urlsafe(12)

                user = self.user_service.create(
                    db,
                    UserCreate(
                        phone=appointment_data.phone_number,
                        password_hash=random_password,
                    ),
                )
                customer = self.customer_repo.first_by(db, user_id=user.id)

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
                    description=appointment_data.description,
                    salon_id=appointment_data.salon_id,
                    start_time=appointment_data.start_time,
                    paid_price=appointment_data.paid_price,
                ),
            )
            for item in appointment_data.service_id:
                self.appintment_service.create(
                    db,
                    AppointmentServiceCreate(
                        appointment_id=appointment.id, service_id=item
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
                raise NotFoundException("Appointment not found")

            return appointment

        except HTTPException:
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
                raise NotFoundException("Appointment not found")

            appointment = self.repo.update(
                db, db_obj=appointment, obj_in=appointment_data
            )

            return appointment

        except HTTPException:
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
                raise NotFoundException("Appointment not found")

            return self.repo.delete(db, appointment_id)

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:

            db.rollback()

            logger.exception(f"Failed to delete appointment {appointment_id}")

            raise InternalServerException("Failed to delete appointment")

    def get_customer_appointment(self, db: Session, user_id, role: str):
        try:
            if role.lower() == "customer":
                customer = self.customer_repo.first_by(db, user_id=user_id)
                if customer is None:
                    raise NotFoundException(messages.NOT_FOUND)

                appointment = self.repo.filter_by(db, customer_id=customer.id)
                logger.info(f"get customer appointment with id : {customer.id} ")
            elif role.lower() == "owner":
                owner = self.owner_repo.first_by(db, user_id=user_id)
                appointment = self.repo.filter_by(db, salon_id=owner.salons[0].id)
                logger.info(f"get customer appointment with id : {owner.salons[0].id} ")

            return appointment
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"failed to get customer appointment with id : {customer.id} ")
            raise InternalServerException(messages.GET_ERROR)

    def pay(self, db: Session, data_in: PayPrice):
        try:

            appointment = self.update(
                db,
                data_in.appointment_id,
                AppointmentUpdate(paid_price=data_in.pay_price),
            )
            wallet = self.wallet.get_by_customer_id(db, data_in.customer_id)
            transaction = self.transaction.create(
                db,
                data_in=WalletTransactionCreate(
                    appointment_id=data_in.appointment_id,
                    amount=data_in.pay_price * Decimal("0.1"),
                    type=WalletTranceactionType.CASHBACK,
                    wallet_id=wallet.id,
                ),
            )
            return appointment
        except Exception as e:
            print(e)
            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)
