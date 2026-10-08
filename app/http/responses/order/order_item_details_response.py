from pydantic import BaseModel

from app.http.responses.types import Price


class OrderItemDetailsResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: Price
    count: int
