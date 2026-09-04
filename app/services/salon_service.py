from app.repositories.salon_repository import SalonRepository
from fastapi import HTTPException
from app.schemas.salon import CustomerFilterOut, SalonCreate, SalonUpdate
from app.models.salon import Salon
from app.exceptions import InternalServerException, NotFoundException
from app.core.messages import messages
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.schemas.salon import CustomerFilter
from app.services.owner_service import OwnerService


class SalonService:

    def __init__(self, repo: SalonRepository, owner_service: OwnerService):
        self.repo = repo
        self.owner_service = owner_service

    def create(self, db: Session, data_in: SalonCreate, user_id: int):
        try:
            owner = self.owner_service.repo.first_by(db, user_id=user_id)
            if owner is None:
                raise NotFoundException(messages.NOT_FOUND)

            data_in.owner_id = owner.id

            salon = self.repo.create(db, data_in)

            logger.info(f"salon created id:{salon.id}")

            return salon

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"failed to create salon: {e}")

            raise InternalServerException(messages.CREATE_ERROR)

    def get(self, db: Session, salon_id: int):
        try:
            salon = self.repo.get_by_id(db, salon_id)

            if not salon:
                logger.warning(f"salon not found id:{salon_id}")

                raise NotFoundException(messages.NOT_FOUND)

            logger.info(f"salon fetched id:{salon_id}")

            return salon

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to get salon id:{salon_id} error:{e}")

            raise InternalServerException(messages.GET_ERROR)

    def get_all(self, db: Session):
        try:
            salons = self.repo.get_all(db)

            logger.info("salons fetched successfully")

            return salons

        except Exception as e:
            logger.error(f"failed to get salons: {e}")

            raise InternalServerException(messages.GET_ERROR)

    def update(self, db: Session, user_id: int, data_in: SalonUpdate):
        try:
            salon = self.get_salon_by_user_id(db, user_id)

            if not salon:
                logger.warning(f"salon not found for update ")

                raise NotFoundException(messages.NOT_FOUND)

            salon = self.repo.update(db, salon, data_in)

            logger.info(f"salon updated id:{salon.id}")

            return salon

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to update salon id:{salon_id} error:{e}")

            raise InternalServerException(messages.UPDATE_ERROR)

    def delete(self, db: Session, salon_id: int):
        try:
            salon = self.repo.get_by_id(db, salon_id)

            if not salon:
                logger.warning(f"salon not found for delete id:{salon_id}")

                raise NotFoundException(messages.NOT_FOUND)

            result = self.repo.delete(db, salon_id)

            logger.info(f"salon deleted id:{salon_id}")

            return result

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to delete salon id:{salon_id} error:{e}")

            raise InternalServerException(messages.DELETE_ERROR)

    def search_customer(
        self, db: Session, user_id: int, user_role: str, filter_data: CustomerFilter
    ):
        try:

            data = self.repo.filter_customer(db, user_id, filter_data)
            return [
                CustomerFilterOut(
                    customer=customer,
                    phone=phone,
                )
                for customer, phone in data
            ]

        except Exception as e:
            logger.error(f"failed to filter customer e -> {e}")
            raise InternalServerException()

    def get_salon_by_user_id(self, db: Session, user_id):
        try:
            salon = self.repo.get_salon_by_user_id(db, user_id)
            if salon is None:
                raise NotFoundException(messages.NOT_FOUND)
            logger.info(f"get salon by user id :{user_id}")
            return salon
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"failed to get salon by user_id e => {e}")
            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)

    def get_services_by_salon_id(self, db: Session, salon_id: int):
        try:
            services = self.repo.get_services_by_salon_id(db, salon_id)
            logger.info("services recived seccussfuly")
            return services
        except Exception as e:
            logger.error(f"failed to get services by salon_id ({salon_id}) e => {e}")
            raise InternalServerException(messages.INTERNAL_SERVER_ERROR)
