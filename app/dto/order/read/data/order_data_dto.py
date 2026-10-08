from dataclasses import dataclass
from decimal import Decimal

from app.dto.order.read.data.order_item_data_dto import OrderItemDataDto
from app.enums.order.order_status import OrderStatus


@dataclass
class OrderDataDto:
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
    items: list[OrderItemDataDto]
