from pydantic import BaseModel


class CartItemDeletedResponse(BaseModel):
    code: int
    message: str