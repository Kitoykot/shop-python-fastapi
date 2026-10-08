from pydantic import BaseModel


class OrderCancelledResponse(BaseModel):
    code: int
    message: str
