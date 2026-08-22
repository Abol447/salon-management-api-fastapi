from app.repositories.salon_repository import SalonRepository
from app.schemas.salon import CustomerFilterOut, SalonCreate, SalonUpdate
from app.models.salon import Salon
from app.exceptions import InternalServerException, NotFoundException
from app.core.messages import messages
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.schemas.salon import CustomerFilter


class SalonService:

    def __init__(self, repo: SalonRepository):
        self.repo = repo

    def create(self, db: Session, data_in: SalonCreate):
        try:
            salon = self.repo.create(db, data_in)

            logger.info(f"salon created id:{salon.id}")

            return salon

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

    def update(self, db: Session, salon_id: int, data_in: SalonUpdate):
        try:
            salon = self.repo.get_by_id(db, salon_id)

            if not salon:
                logger.warning(f"salon not found for update id:{salon_id}")

                raise NotFoundException(messages.NOT_FOUND)

            salon = self.repo.update(db, salon, data_in)

            logger.info(f"salon updated id:{salon_id}")

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
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                )
                for customer, first_name, last_name, phone in data
            ]

        except Exception as e:
            raise InternalServerException()
