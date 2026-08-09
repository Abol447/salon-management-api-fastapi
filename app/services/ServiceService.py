from sqlalchemy.orm import Session
from app.exceptions import InternalServerException, NotFoundException
from app.models.services import Service
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.services import ServiceCreate, ServiceUpdate
from app.core.logger import logger


class ServiceService:

    def __init__(self, repo: CRUDBase[Service, ServiceCreate, ServiceUpdate]):
        self.repo = repo

    def create_service(self, db: Session, service_in: ServiceCreate):
        try:
            return self.repo.create(db, obj_in=service_in)

        except Exception as e:
            logger.exception(f"Error creating service: {e}")
            raise InternalServerException()

    def get_service(self, db: Session, service_id: int):
        try:
            service = self.repo.get_by_id(db, service_id)

            return service

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
            service = self.repo.get_by_id(db, service_id)

            if not service:
                raise NotFoundException("services")

            return self.repo.remove(db, id=service_id)

        except Exception as e:
            logger.exception(f"Error deleting service {service_id}: {e}")
            raise InternalServerException()
