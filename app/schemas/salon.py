from pydantic import BaseModel, ConfigDict


class SalonCreate(BaseModel):
    name: str
    location: str
    owner_id: int


class SalonUpdate(BaseModel):
    name: str | None = None
    location: str | None = None


class SalonResponse(BaseModel):
    id: int
    name: str
    location: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
