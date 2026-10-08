import math

from app.dto.order.read.data.order_data_dto import OrderDataDto
from app.dto.order.read.order_details_dto import OrderDetailsDto
from app.dto.order.read.order_list_dto import OrderListDto
from app.dto.order.read.order_status_dto import OrderStatusDto
from app.dto.pagination.pagination_dto import PaginationDto
from app.exceptions.order.order_not_found_exception import OrderNotFoundException
from app.repositories.order.order_repository import OrderRepository


class GetOrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def get_order_list(
        self,
        user_id: int,
        page: int,
        per_page: int,
    ) -> tuple[list[OrderListDto], PaginationDto]:
        total_count = self.repository.count_user_orders(user_id)
        if total_count == 0:
            return [], PaginationDto(
                page=page,
                per_page=per_page,
                total=0,
                pages=0,
            )

        orders = self.repository.get_order_list(
            user_id=user_id,
            limit=per_page,
            offset=(page - 1) * per_page,
        )

        order_list = [self.__to_list_dto(order) for order in orders]

        pagination = PaginationDto(
            page=page,
            per_page=per_page,
            total=total_count,
            pages=math.ceil(total_count / per_page),
        )

        return (order_list, pagination)

    def get_order_details(self, order_id: int, user_id: int) -> OrderDetailsDto:
        order = self.repository.get_order_details(order_id=order_id, user_id=user_id)

        if order is None:
            raise OrderNotFoundException()

        return self.__to_details_dto(order)

    def __to_list_dto(self, order: OrderDataDto) -> OrderListDto:
        return OrderListDto(
            id=order.id,
            positions_count=len(order.items),
            status=OrderStatusDto(code=order.status.value, label=order.status.label),
            total_price=order.total_price,
            created_at=order.created_at,
            items=order.items,
        )

    def __to_details_dto(self, order: OrderDataDto) -> OrderDetailsDto:
        return OrderDetailsDto(
            id=order.id,
            status=OrderStatusDto(code=order.status.value, label=order.status.label),
            user_name=order.user_name,
            user_phone_number=order.user_phone_number,
            user_email=order.user_email,
            user_city=order.user_city,
            user_address=order.user_address,
            total_price=order.total_price,
            created_at=order.created_at,
            items=order.items,
        )
