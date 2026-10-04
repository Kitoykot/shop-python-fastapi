from decimal import Decimal

from pydantic import BaseModel, field_serializer


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    name: str
    count: int
    price: Decimal
    is_available: bool

    @field_serializer('price', when_used='json')
    def serialize_price(self, value: Decimal) -> float:
        return float(value)
