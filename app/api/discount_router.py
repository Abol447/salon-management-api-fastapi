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

router = APIRouter(prefix="/discount", tags=["discount"])


def get_discount_service():
    repo = CRUDBase(Discount)
    return DiscountService(repo)


@router.post("", response_model=DiscountResponse)
def create_discount(
    discount_data: DiscountCreate,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    return service.create(db, discount_data)


@router.get("", response_model=list[DiscountResponse])
def get_all_discount(
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    return service.get_all(db)


@router.get("/{discount_id}", response_model=DiscountResponse)
def get_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    return service.get(db, discount_id)


@router.put("/{discount_id}", response_model=DiscountResponse)
def update_discount(
    discount_id: int,
    discount_data: DiscountUpdate,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    return service.update(db, discount_id, discount_data)


@router.delete("/{discount_id}", response_model=DiscountResponse)
def delete_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    service: DiscountService = Depends(get_discount_service),
):
    return service.delete(db, discount_id)
