from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductDataDto:
    id: int
    name: str
    description: str | None
    price: Decimal
    show_in_catalog: bool
    count: int
    is_available: bool
