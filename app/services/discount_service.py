from app.schemas.discount import DiscountCreate, DiscountUpdate
from app.models.discount import Discount
from app.repositories.base.CRUDBase import CRUDBase
from fastapi import HTTPException
from app.exceptions import InternalServerException, NotFoundException
from app.core.logger import logger
from sqlalchemy.orm import Session


class DiscountService:

    def __init__(self, repo: CRUDBase[Discount, DiscountCreate, DiscountUpdate]):
        self.repo = repo

    def create(self, db: Session, discount_data: DiscountCreate):
        try:
            discount = self.repo.create(db, discount_data)

            logger.info(f"discount with id: {discount.id} created successfully")

            return discount

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"failed to create discount: {e}")

            raise InternalServerException("failed to create discount")

    def get(self, db: Session, discount_id: int):
        try:
            discount = self.repo.get_by_id(db, discount_id)

            if not discount:
                logger.warning(f"discount with id: {discount_id} not found")

                raise NotFoundException(f"discount with id: {discount_id} not found")

            logger.info(f"discount with id: {discount_id} fetched successfully")

            return discount

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"failed to get discount with id {discount_id}: {e}")

            raise InternalServerException("failed to get discount")

    def get_all(self, db: Session):
        try:
            discounts = self.repo.get_all(db)

            logger.info("all discounts fetched successfully")

            return discounts

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"failed to get all discounts: {e}")

            raise InternalServerException("failed to get all discounts")

    def update(self, db: Session, discount_id: int, discount_data: DiscountUpdate):
        try:
            discount = self.repo.get_by_id(db, discount_id)

            if not discount:
                logger.warning(f"discount with id: {discount_id} not found")

                raise NotFoundException(f"discount with id: {discount_id} not found")

            updated_discount = self.repo.update(db, discount, discount_data)

            logger.info(f"discount with id: {discount_id} updated successfully")

            return updated_discount

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"failed to update discount with id {discount_id}: {e}")

            raise InternalServerException("failed to update discount")

    # DELETE
    def delete(self, db: Session, discount_id: int):
        try:
            discount = self.repo.get_by_id(db, discount_id)

            if not discount:
                logger.warning(f"discount with id: {discount_id} not found")

                raise NotFoundException(f"discount with id: {discount_id} not found")

            response = self.repo.delete(db, discount)

            logger.info(f"discount with id: {discount_id} deleted successfully")

            return response

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"failed to delete discount with id {discount_id}: {e}")

            raise InternalServerException("failed to delete discount")
