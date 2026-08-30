from sqlalchemy.orm import Session
from app.exceptions import InternalServerException, NotFoundException
from app.models.services import Service
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.services import ServiceCreate, ServiceUpdate
from app.core.logger import logger
from app.exceptions import BadRequestException
from app.core.messages import messages
from app.services.salon_service import SalonService
from app.services.owner_service import OwnerService
from fastapi import HTTPException


class ServiceService:

    def __init__(
        self,
        repo: CRUDBase[Service, ServiceCreate, ServiceUpdate],
        salon_service: SalonService,
        owner_service: OwnerService,
    ):
        self.repo = repo
        self.salon_service = salon_service
        self.owner_service = owner_service

    def create_service(
        self, db: Session, service_in: ServiceCreate, user_id: int, user_role: str
    ):
        try:
            print(user_role)
            if user_role != "owner":
                raise BadRequestException(messages.TOKEN_INVALID)
            owner = self.owner_service.repo.first_by(db, user_id=user_id)
            salon = self.salon_service.repo.first_by(db, owner_id=owner.id)
            if salon is None:
                raise BadRequestException(messages.NOT_FOUND)
            service_in.salon_id = salon.id
            return self.repo.create(db, obj_in=service_in)
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Error creating service: {e}")
            raise InternalServerException()

    def get_service(self, db: Session, service_id: int):
        try:
            service = self.repo.get_by_id(db, service_id)
            if service is None:
                raise BadRequestException(messages.SERVICE_NOT_FOUND)

            return service
        except HTTPException:
            raise

        except Exception as e:
            logger.exception(f"Error getting service {service_id}: {e}")
            raise InternalServerException()

    def get_services(self, db: Session):
        try:
            return self.repo.get_all(db)

        except Exception as e:
            logger.exception(f"Error getting services: {e}")
            raise InternalServerException()

    def update_service(self, db: Session, service_id: int, service_in: ServiceUpdate):
        try:
            service = self.repo.get_by_id(db, service_id)

            if not service:
                raise NotFoundException("services")

            return self.repo.update(db, db_obj=service, obj_in=service_in)

        except Exception as e:
            logger.exception(f"Error updating service {service_id}: {e}")
            raise InternalServerException()

    def delete_service(self, db: Session, service_id: int):
        try:

            return self.repo.delete(db, service_id)

        except Exception as e:
            logger.exception(f"Error deleting service {service_id}: {e}")
            raise InternalServerException()
