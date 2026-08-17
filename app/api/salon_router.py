from app.services.salon_service import Salon, SalonCreate, SalonUpdate, SalonService
from app.repositories.base.CRUDBase import CRUDBase
from app.db.database import get_db
from fastapi import APIRouter, Depends
from app.schemas.response import ResponseSchema
from app.schemas.salon import SalonResponse
from sqlalchemy.orm import Session
from app.core.messages import messages

router = APIRouter(prefix="/salon", tags=["salon"])


def get_service():
    repo = CRUDBase(Salon)
    return SalonService(repo)


@router.post("", response_model=ResponseSchema[SalonResponse])
def create(
    data_in: SalonCreate,
    db: Session = Depends(get_db),
    service: SalonService = Depends(get_service),
):
    data = service.create(db, data_in)
    return ResponseSchema(data=data, message=messages.CREATED)
