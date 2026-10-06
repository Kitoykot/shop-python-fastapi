from pydantic import BaseModel


class OrderCreatedResponse(BaseModel):
    code: int
    message: str
