from app.services.salon_service import Salon, SalonCreate, SalonUpdate, SalonService
from app.repositories.salon_repository import SalonRepository
from app.db.database import get_db
from fastapi import APIRouter, Depends
from app.schemas.response import ResponseSchema
from app.schemas.salon import SalonResponse, CustomerFilterOut, CustomerFilter
from sqlalchemy.orm import Session
from app.core.messages import messages
from app.dependencies.auth import get_current_user, require_roles
from app.schemas.services import ServiceOut

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
    user: dict = Depends(require_roles("owner")),
):
    return ResponseSchema(
        data=service.search_customer(
            db, user_id=user["sub"], user_role=user["role"], filter_data=filter
        ),
        message=messages.GET_ALL,
    )


@router.put("", response_model=ResponseSchema[SalonResponse])
def update(
    data_in: SalonUpdate,
    user: dict = Depends(require_roles("owner")),
    db: Session = Depends(get_db),
    service: SalonService = Depends(get_service),
):
    return ResponseSchema(
        data=service.update(db, user["sub"], data_in), message=messages.UPDATED
    )


@router.get("/user_id", response_model=ResponseSchema[SalonResponse])
def get_by_user_id(
    user: dict = Depends(require_roles("owner")),
    db: Session = Depends(get_db),
    service: SalonService = Depends(get_service),
):
    return ResponseSchema(
        data=service.get_salon_by_user_id(db, user["sub"]), message=messages.GET_ALL
    )


@router.get("/{salon-id}/services", response_model=ResponseSchema[list[ServiceOut]])
def get_services_by_salon_id(
    salon_id: int,
    db: Session = Depends(get_db),
    service: SalonService = Depends(get_service),
):
    return ResponseSchema(
        message=messages.GET_ALL, data=service.get_services_by_salon_id(db, salon_id)
    )
