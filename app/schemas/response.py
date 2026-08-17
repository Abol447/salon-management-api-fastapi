from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    data: T | None = None
    message: str | None = None
