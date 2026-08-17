from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse


class OwnerCreate(BaseModel):
    user_id: int


class OwnerUpdate(BaseModel):
    user_id: int | None = None


class OwnerResponse(BaseModel):
    id: int
    user_id: int
    user: UserResponse
    model_config = ConfigDict(from_attributes=True)
