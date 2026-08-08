from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CustomerCreate(BaseModel):
    birthday: datetime | None = None
    profile_image: str | None = None
    user_id: int


class CustomerUpdate(BaseModel):
    birthday: datetime | None = None
    profile_image: str | None = None


class CustomerResponse(BaseModel):
    id: int
    birthday: datetime | None = None
    profile_image: str | None = None
    user_id: int

    model_config = ConfigDict(from_attributes=True)