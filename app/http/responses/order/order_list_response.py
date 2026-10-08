from pydantic import BaseModel

from app.http.responses.order.order_response import OrderResponse
from app.http.responses.pagination.pagination_response import PaginationResponse


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
    pagination: PaginationResponse
