from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.discount import Discount
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.discount import (
    DiscountCreate,
    DiscountUpdate,
    DiscountResponse,
)
from app.services.discount_service import DiscountService
from app.core.messages import messages
from app.schemas.response import ResponseSchema

router = APIRouter(prefix="/discount", tags=["discount"])


def get_discount_service():
    repo = CRUDBase(Discount)
    return DiscountService(repo)


@router.post("", response_model=ResponseSchema[DiscountResponse])
def create_discount(
    discount_data: DiscountCreate,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    data = service.create(db, discount_data)

    return ResponseSchema(data=data, message=messages.DISCOUNT_CREATED)


@router.get("", response_model=ResponseSchema[list[DiscountResponse]])
def get_all_discount(
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    data = service.get_all(db)

    return ResponseSchema(data=data, message=messages.DISCOUNTS_FOUND)


@router.get("/{discount_id}", response_model=ResponseSchema[DiscountResponse])
def get_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    data = service.get(db, discount_id)

    return ResponseSchema(data=data, message=messages.DISCOUNT_FOUND)


@router.put("/{discount_id}", response_model=ResponseSchema[DiscountResponse])
def update_discount(
    discount_id: int,
    discount_data: DiscountUpdate,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    data = service.update(db, discount_id, discount_data)

    return ResponseSchema(data=data, message=messages.DISCOUNT_UPDATED)


@router.delete("/{discount_id}", response_model=ResponseSchema[DiscountResponse])
def delete_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    data = service.delete(db, discount_id)

    return ResponseSchema(data=data, message=messages.DISCOUNT_DELETED)
