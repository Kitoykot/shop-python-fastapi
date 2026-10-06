from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.dto.order.create_order_item_dto import CreateOrderItemDto
from app.dto.order.order_create_data_dto import OrderCreateDataDto
from app.enums.order.order_status import OrderStatus
from app.models.order.order import Order
from app.models.order.order_item import OrderItem


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session


    def create_order_during_transaction(self, dto: OrderCreateDataDto) -> None:
        order = Order(
            user_id=dto.user_id,
            status=OrderStatus.NEW,
            user_name=dto.user_name,
            user_phone_number=dto.user_phone_number,
            user_email=dto.user_email,
            user_city=dto.user_city,
            user_address=dto.user_address,
            total_price=dto.total_price,
            created_at=datetime.now(UTC),
            items=[
                self.__to_order_item_model(item_dto=item) 
                for item in dto.items
            ]
        )

        self.session.add(order)


    def __to_order_item_model(self, item_dto: CreateOrderItemDto) -> OrderItem:
        return OrderItem(
            product_id=item_dto.product_id,
            product_name=item_dto.product_name,
            price=item_dto.price,
            count=item_dto.count,
        )