from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateOrderItemDto:
    product_id: int
    product_name: str
    price: Decimal
    count: int
