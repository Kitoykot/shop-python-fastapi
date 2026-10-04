from decimal import Decimal

from pydantic import BaseModel, field_serializer


class CartResponse(BaseModel):
    items_count: int
    total_price: Decimal

    @field_serializer('total_price', when_used='json')
    def serialize_totle_price(self, value: Decimal) -> float:
        return float(value)
