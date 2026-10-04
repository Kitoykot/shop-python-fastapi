from dataclasses import dataclass
from decimal import Decimal

from pydantic import field_serializer


@dataclass
class ProductDto:
    id: int | None
    name: str
    description: str | None
    price: Decimal
    show_in_catalog: bool
    count: int
    is_available: bool

    @field_serializer('price', when_used='json')
    def serialize_price(self, value: Decimal) -> float:
        return float(value)
