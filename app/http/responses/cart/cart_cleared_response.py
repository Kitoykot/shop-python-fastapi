from pydantic import BaseModel


class CartClearedResponse(BaseModel):
    code: int
    message: str
