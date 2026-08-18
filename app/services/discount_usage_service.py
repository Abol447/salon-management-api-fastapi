from app.models.discount_usage import DiscountUsage
from app.schemas.discount_usage import DiscountUsageCreate, DiscountUsageUpdate
from app.repositories.base.CRUDBase import CRUDBase
from app.services.discount_service import DiscountService
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.core.messages import messages
from app.exceptions import InternalServerException


class DiscountUsageService:

    def __init__(
        self,
        repo: CRUDBase[DiscountUsage, DiscountUsageCreate, DiscountUsageUpdate],
    ):
        self.repo = repo

    def create(self, db: Session, data_in: DiscountUsageCreate):
        try:
            discount_usage = self.repo.create(db, data_in)
            logger.info(
                f"discount ({data_in.discount_id}) by customer ({data_in.customer_id})"
            )
            return discount_usage
        except Exception as e:
            logger.error(
                f"failed to create discount_usage for customer {data_in.customer_id} => {e}"
            )
            raise InternalServerException(messages.DISCOUNT_USAGE_CREATE_FAILED)
