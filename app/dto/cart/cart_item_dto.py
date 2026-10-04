from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CartItemDto:
    id: int
    product_id: int
    name: str
    count: int
    price: Decimal
    is_available: bool
