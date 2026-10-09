from dataclasses import dataclass
from decimal import Decimal

from app.dto.order.read.data.order_item_data_dto import OrderItemDataDto
from app.dto.order.read.order_status_dto import OrderStatusDto


@dataclass
class OrderDetailsDto:
    id: int
    status: OrderStatusDto
    user_name: str
    user_phone_number: str
    user_email: str | None
    user_city: str
    user_address: str
    total_price: Decimal
    can_be_paid: bool
    created_at: str
    items: list[OrderItemDataDto]
