from decimal import Decimal

from pydantic import BaseModel, field_serializer

from app.http.responses.order.order_item_response import OrderItemResponse
from app.http.responses.order.order_status_response import OrderStatusResponse


class OrderResponse(BaseModel):
    id: int
    positions_count: int
    status: OrderStatusResponse
    total_price: Decimal
    created_at: str
    items: list[OrderItemResponse]

    @field_serializer('total_price', when_used='json')
    def seriflize_total_price(self, value: Decimal) -> float:
        return float(value)
