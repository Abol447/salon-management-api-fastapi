from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse


class CustomerCreate(BaseModel):
    birthday: datetime | None = None
    profile_image: str | None = None
    user_id: int
    salon_id : int
    first_name: str | None = None
    last_name: str | None = None


class CustomerUpdate(BaseModel):
    birthday: datetime | None = None
    profile_image: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class CustomerResponse(BaseModel):
    id: int
    birthday: datetime | None = None
    profile_image: str | None = None
    first_name: str | None = None
    user: UserResponse

    last_name: str | None = None
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class GetCustomerAppointment(BaseModel):
    customer_id: int
