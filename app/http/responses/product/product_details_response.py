from decimal import Decimal

from pydantic import BaseModel, field_serializer


class ProductDetailsResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: Decimal
    is_available: bool

    @field_serializer('price', when_used='json')
    def serialize_price(self, value: Decimal) -> float:
        return float(value)
