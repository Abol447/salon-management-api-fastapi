from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    role_id: int | None = None
    user_name: Optional[str] = None


class UserCreate(UserBase):
    password_hash: str


class SystemUserCreate(BaseModel):
    phone: str
    password_hash: str
    role_id: int


class UserUpdate(BaseModel):

    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int

    phone: str
    user_name: Optional[str] = None
    email: Optional[EmailStr]
    is_active: bool
    role_id: int
    model_config = ConfigDict(from_attributes=True)
