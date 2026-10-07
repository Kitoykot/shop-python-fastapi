from dataclasses import dataclass
from decimal import Decimal

from app.dto.order.order_item_dto import OrderItemDto
from app.enums.order.order_status import OrderStatus


@dataclass
class OrderDto:
    id: int
    user_id: int
    status: OrderStatus
    user_name: str
    user_phone_number: str
    user_email: str | None
    user_city: str
    user_address: str
    total_price: Decimal
    created_at: str
    items: list[OrderItemDto]
