from decimal import Decimal

from pydantic import BaseModel, field_serializer


class ProductListResponse(BaseModel):
    id: int
    name: str
    price: Decimal

    @field_serializer('price', when_used='json')
    def serialize_price(self, value: Decimal) -> float:
        return float(value)
