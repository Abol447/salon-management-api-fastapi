from app.services.salon_service import Salon, SalonCreate, SalonUpdate, SalonService
from app.repositories.salon_repository import SalonRepository
from app.db.database import get_db
from fastapi import APIRouter, Depends
from app.schemas.response import ResponseSchema
from app.schemas.salon import SalonResponse, CustomerFilterOut, CustomerFilter
from sqlalchemy.orm import Session
from app.core.messages import messages
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/salon", tags=["salon"])


def get_service():
    repo = SalonRepository()
    return SalonService(repo)


@router.post("", response_model=ResponseSchema[SalonResponse])
def create(
    data_in: SalonCreate,
    db: Session = Depends(get_db),
    service: SalonService = Depends(get_service),
):
    data = service.create(db, data_in)
    return ResponseSchema(data=data, message=messages.CREATED)


@router.get("/search", response_model=ResponseSchema[list[CustomerFilterOut]])
def search(
    filter: CustomerFilter = Depends(),
    db: Session = Depends(get_db),
    service: SalonService = Depends(get_service),
    user: dict = Depends(get_current_user),
):
    return ResponseSchema(
        data=service.search_customer(
            db, user_id=user["sub"], user_role=user["role"], filter_data=filter
        ),
        message=messages.GET_ALL,
    )
