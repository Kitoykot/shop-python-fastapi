from dataclasses import dataclass
from decimal import Decimal

from app.dto.order.read.data.order_item_data_dto import OrderItemDataDto
from app.dto.order.read.order_status_dto import OrderStatusDto


@dataclass
class OrderListDto:
    id: int
    positions_count: int
    status: OrderStatusDto
    created_at: str
    total_price: Decimal
    items: list[OrderItemDataDto]
