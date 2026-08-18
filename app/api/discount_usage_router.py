from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session


from app.models.discount_usage import DiscountUsage
from app.services.discount_usage_service import (
    DiscountUsageService,
    DiscountUsageCreate,
    DiscountUsageUpdate,
)
from app.schemas.response import ResponseSchema
from app.schemas.discount_usage import DiscountUsageOut
from app.db.database import get_db
from app.repositories.base.CRUDBase import CRUDBase
from app.core.messages import messages

router = APIRouter(prefix="/discount-usage", tags=["discount-usage"])


def get_service():
    repo = CRUDBase(DiscountUsage)
    return DiscountUsageService(repo)


@router.post("", response_model=ResponseSchema[DiscountUsageOut])
def create(
    data_in: DiscountUsageCreate,
    service: DiscountUsageService = Depends(get_service),
    db: Session = Depends(get_db),
):
    data = service.create(db, data_in)
    return ResponseSchema(data=data, message=messages.DISCOUNT_USAGE_CREATED)
