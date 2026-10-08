from pydantic import BaseModel

from app.http.responses.order.order_item_response import OrderItemResponse
from app.http.responses.order.order_status_response import OrderStatusResponse
from app.http.responses.types import Price


class OrderResponse(BaseModel):
    id: int
    positions_count: int
    status: OrderStatusResponse
    total_price: Price
    created_at: str
    items: list[OrderItemResponse]
