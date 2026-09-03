from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServiceCreate(BaseModel):
    name: str
    is_active: bool = True
    salon_id: int | None = None


class ServiceUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class ServiceRes(BaseModel):
    id: int
    name: str


class ServiceOut(BaseModel):
    id: int
    name: str
    salon_id: int
    is_active: bool
    CreatedAt: datetime
    model_config = ConfigDict(from_attributes=True)
