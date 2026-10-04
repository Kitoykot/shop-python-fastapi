from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CartDto:
    items_count: int
    total_price: Decimal
