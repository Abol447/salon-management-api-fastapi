from pydantic import BaseModel


class LoginSchema(BaseModel):
    phone_number: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class LogOutSchema(BaseModel):
    refresh_token: str
