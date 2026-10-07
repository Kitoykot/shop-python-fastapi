from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderItemDto:
    id: int
    order_id: int
    product_id: int
    product_name: str
    price: Decimal
    count: int
