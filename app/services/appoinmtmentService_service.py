from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.AppointmentService import (
    AppointmentServiceCreate,
    AppointmentServiceUpdate,
)
from app.models.AppointmentService import AppointmentService
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.exceptions import InternalServerException, NotFoundException
from app.core.messages import messages
from fastapi import HTTPException


class AppointmentService_service:

    def __init__(
        self,
        repo: CRUDBase[
            AppointmentService, AppointmentServiceCreate, AppointmentServiceUpdate
        ],
    ):
        self.repo = repo

    def create(self, db: Session, data_in: AppointmentServiceCreate):
        try:
            service = self.repo.create(db, data_in)

            logger.info(f"appointment_service created id={service.id}")

            return service

        except Exception as e:
            logger.error(f"failed to create appointment_service: {e}")

            raise InternalServerException("failed to create appointment_service")

    def get(self, db: Session, appointment_service_id: int):
        try:
            service = self.repo.get_by_id(db, appointment_service_id)

            if not service:
                logger.warning(
                    f"appointment_service not found id={appointment_service_id}"
                )
                raise NotFoundException(messages.NOT_FOUND)

            return service
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                f"failed to get appointment_service "
                f"id={appointment_service_id}: {e}"
            )

            raise InternalServerException("failed to get appointment_service")

    def get_all(self, db: Session):
        try:
            services = self.repo.get_all(db)

            logger.info("appointment_services fetched successfully")

            return services

        except Exception as e:
            logger.error(f"failed to get appointment_services: {e}")

            raise InternalServerException("failed to get appointment_services")

    def update(
        self,
        db: Session,
        appointment_service_id: int,
        data_in: AppointmentServiceUpdate,
    ):
        try:
            service = self.repo.get_by_id(db, appointment_service_id)

            if not service:
                logger.warning(
                    f"appointment_service not found " f"id={appointment_service_id}"
                )
                raise NotFoundException(messages.NOT_FOUND)

            updated_service = self.repo.update(db, service, data_in)

            logger.info(f"appointment_service updated " f"id={appointment_service_id}")

            return updated_service
        except HTTPException:
            raise

        except Exception as e:
            logger.error(
                f"failed to update appointment_service "
                f"id={appointment_service_id}: {e}"
            )

            raise InternalServerException("failed to update appointment_service")

    def delete(self, db: Session, appointment_service_id: int):
        try:
            appointment = self.get(db, appointment_service_id)
            service = self.repo.delete(db, appointment)

            logger.info(f"appointment_service deleted " f"id={appointment_service_id}")

            return service

        except Exception as e:
            logger.error(
                f"failed to delete appointment_service "
                f"id={appointment_service_id}: {e}"
            )

            raise InternalServerException("failed to delete appointment_service")
