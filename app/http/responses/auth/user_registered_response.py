from pydantic import BaseModel


class UserRegisteredResponse(BaseModel):
    code: int
    message: str
