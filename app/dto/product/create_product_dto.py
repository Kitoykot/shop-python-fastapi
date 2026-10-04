from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateProductDto:
    name: str
    description: str | None
    price: Decimal
    count: int
