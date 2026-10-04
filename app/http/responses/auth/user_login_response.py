from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_at: str
    refresh_token_expires_at: str
