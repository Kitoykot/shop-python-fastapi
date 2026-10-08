from pydantic import BaseModel

from app.http.responses.types import Price


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    name: str
    count: int
    price: Price
    is_available: bool
