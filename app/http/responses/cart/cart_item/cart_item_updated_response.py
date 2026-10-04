from pydantic import BaseModel


class CartItemUpdatedResponse(BaseModel):
    code: int
    message: str
