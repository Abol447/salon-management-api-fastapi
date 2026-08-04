from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TokenBase(BaseModel):
    pass


class refresh_token (BaseModel):
    refresh_token : str
    

class TokenCreate(TokenBase):
    user_id: int



class TokenUpdate(BaseModel):
    revoked: bool | None = None



class TokenResponse(TokenBase):
    id: int
    user_id: int
    refresh_token: str
    expires_at: datetime
    revoked: bool
    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )