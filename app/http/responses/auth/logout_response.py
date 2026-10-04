from pydantic import BaseModel


class LogoutResponse(BaseModel):
    code: int
    message: str