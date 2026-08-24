from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.base.CRUDBase import CRUDBase
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

from app.exceptions import InternalServerException, NotFoundException
from app.schemas.customer import GetCustomerAppointment
from app.models.appointment import Appointment
from app.schemas.Appointment import AppointmentCreate, AppointmentUpdate
from app.core.logger import logger
from app.services.salon_service import SalonService
from app.core.messages import messages
from app.services.owner_service import OwnerService


class CustomerService:

    def __init__(
        self,
        repo: CRUDBase[Customer, CustomerCreate, CustomerUpdate],
        appointment_repo: CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate],
        salon_service: SalonService,
        owner_service: OwnerService,
    ):
        self.repo = repo
        self.appointment_repo = appointment_repo
        self.salon_service = salon_service
        self.owner_service = owner_service

    def create(self, db: Session, customer_data: CustomerCreate):

        try:

            customer = self.repo.create(db, customer_data)

            logger.info(f"customer created successfully id={customer.id}")

            return customer

        except HTTPException:
            raise

        except Exception as e:

            logger.error(f"failed to create customer: {e}")

            raise InternalServerException("failed to create customer")

    def get(self, db: Session, customer_id: int):

        try:

            customer = self.repo.get_by_id(db, customer_id)

            if not customer:

                logger.warning(f"customer not found id={customer_id}")

                raise NotFoundException(f"customer with id={customer_id} not found")

            logger.info(f"customer fetched successfully id={customer_id}")

            return customer

        except HTTPException:
            raise

        except Exception as e:

            logger.error(f"failed to get customer id={customer_id}: {e}")

            raise InternalServerException("failed to get customer")

    def get_by_user_id(self, db: Session, user_id: int):

        try:

            customer = self.repo.first_by(db, user_id=user_id)

            if not customer:

                logger.warning(f"customer not found for user_id={user_id}")

                raise NotFoundException(f"customer for user_id={user_id} not found")

            logger.info(f"customer fetched successfully user_id={user_id}")

            return customer

        except HTTPException:
            raise

        except Exception as e:

            logger.error(f"failed to get customer by user_id={user_id}: {e}")

            raise InternalServerException("failed to get customer")

    def get_all(self, db: Session):

        try:

            customers = self.repo.get_all(db)

            logger.info("customers fetched successfully")

            return customers

        except HTTPException:
            raise

        except Exception as e:

            logger.error(f"failed to get customers: {e}")

            raise InternalServerException("failed to get customers")

    def update(self, db: Session, customer_data: CustomerUpdate, user_id: int):

        try:

            customer = self.repo.first_by(db, user_id=user_id)

            if customer is None:

                logger.warning(f"customer not found for user_id={user_id}")

                raise NotFoundException(f"customer for user_id={user_id} not found")

            customer_update = self.repo.update(db, customer, customer_data)

            logger.info(f"customer updated successfully id={customer.id}")

            return customer_update

        except HTTPException:
            raise

        except Exception as e:

            logger.error(f"failed to update customer " f"user_id={user_id}: {e}")

            raise InternalServerException("failed to update customer")

    def delete(self, db: Session, customer_id: int):

        try:

            customer = self.repo.get_by_id(db, customer_id)

            if customer is None:

                logger.warning(f"customer not found for delete id={customer_id}")

                raise NotFoundException(f"customer with id={customer_id} not found")

            response = self.repo.delete(db, customer)

            logger.info(f"customer deleted successfully id={customer_id}")

            return response

        except HTTPException:
            raise

        except Exception as e:

            logger.error(f"failed to delete customer " f"id={customer_id}: {e}")

            raise InternalServerException("failed to delete customer")

    def get_appointment(
        self, db: Session, data_in: GetCustomerAppointment, owner_id: int
    ):
        try:
            owner = self.owner_service.repo.first_by(db, user_id=owner_id)
            salon = self.salon_service.repo.first_by(db, owner_id=owner.id)
            if salon is None:
                raise NotFoundException(messages.NOT_FOUND)
            appointment = self.appointment_repo.filter_by(
                db, customer_id=data_in.customer_id, salon_id=salon.id
            )
            logger.info(f"get customer {data_in.customer_id} appointment")
            return appointment
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                f"failed to get customer {data_in.customer_id} appointment e => {e} "
            )
            raise InternalServerException()
