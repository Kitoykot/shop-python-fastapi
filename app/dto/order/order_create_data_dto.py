from dataclasses import dataclass
from decimal import Decimal

from app.dto.order.create_order_item_dto import CreateOrderItemDto


@dataclass
class OrderCreateDataDto:
    user_id: int
    user_name: str
    user_phone_number: str
    user_email: str | None
    user_city: str
    user_address: str
    total_price: Decimal
    items: list[CreateOrderItemDto]
