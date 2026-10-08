from pydantic import BaseModel

from app.http.responses.types import Price


class CartResponse(BaseModel):
    items_count: int
    total_price: Price
