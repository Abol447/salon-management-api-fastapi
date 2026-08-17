from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerUpdate
from app.repositories.base.CRUDBase import CRUDBase
from sqlalchemy.orm import Session
from app.exceptions import InternalServerException, NotFoundException
from app.core.logger import logger
from app.core.messages import messages


class OwnerService:

    def __init__(self, repo: CRUDBase[Owner, OwnerCreate, OwnerUpdate]):
        self.repo = repo

    def create(self, db: Session, data_in: OwnerCreate):
        try:
            owner = self.repo.create(db, data_in)

            logger.info(f"owner created id : {owner.id}")

            return owner

        except Exception as e:
            logger.error(f"failed to create owner e => {e}")

            raise InternalServerException(messages.CREATE_ERROR)

    def get(self, db: Session, owner_id: int):
        try:
            owner = self.repo.get_by_id(db, owner_id)

            if not owner:
                logger.warning(f"owner not found id : {owner_id}")

                raise NotFoundException(messages.NOT_FOUND)

            logger.info(f"owner fetched id : {owner_id}")

            return owner

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to get owner id : {owner_id} e => {e}")

            raise InternalServerException(messages.GET_ERROR)

    def get_all(self, db: Session):
        try:
            owners = self.repo.get_all(db)

            logger.info("owners fetched successfully")

            return owners

        except Exception as e:
            logger.error(f"failed to get owners e => {e}")

            raise InternalServerException(messages.GET_ERROR)

    def update(self, db: Session, owner_id: int, data_in: OwnerUpdate):
        try:
            owner = self.repo.get_by_id(db, owner_id)

            if not owner:
                logger.warning(f"owner not found for update id : {owner_id}")

                raise NotFoundException(messages.NOT_FOUND)

            owner = self.repo.update(db, owner, data_in)

            logger.info(f"owner updated id : {owner_id}")

            return owner

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to update owner id : {owner_id} e => {e}")

            raise InternalServerException(messages.UPDATE_ERROR)

    def delete(self, db: Session, owner_id: int):
        try:
            owner = self.repo.get_by_id(db, owner_id)

            if not owner:
                logger.warning(f"owner not found for delete id : {owner_id}")

                raise NotFoundException(messages.NOT_FOUND)

            owner = self.repo.delete(db, owner_id)

            logger.info(f"owner deleted id : {owner_id}")

            return owner

        except NotFoundException:
            raise

        except Exception as e:
            logger.error(f"failed to delete owner id : {owner_id} e => {e}")

            raise InternalServerException(messages.DELETE_ERROR)
