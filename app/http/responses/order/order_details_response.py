from pydantic import BaseModel

from app.dto.order.read.order_status_dto import OrderStatusDto
from app.http.responses.order.order_item_details_response import (
    OrderItemDetailsResponse,
)
from app.http.responses.types import Price


class OrderDetailsResponse(BaseModel):
    id: int
    status: OrderStatusDto
    user_name: str
    user_phone_number: str
    user_email: str | None
    user_city: str
    user_address: str
    total_price: Price
    created_at: str
    items: list[OrderItemDetailsResponse]
