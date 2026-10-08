from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session, selectinload

from app.dto.order.create.create_order_item_dto import CreateOrderItemDto
from app.dto.order.create.order_create_data_dto import OrderCreateDataDto
from app.dto.order.read.data.order_data_dto import OrderDataDto
from app.dto.order.read.data.order_item_data_dto import OrderItemDataDto
from app.enums.order.order_status import OrderStatus
from app.models.order.order import Order
from app.models.order.order_item import OrderItem


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_order_list(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> list[OrderDataDto]:
        statement = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.id.desc())
            .limit(limit)
            .offset(offset)
        )

        orders = self.session.scalars(statement).all()
        return [self.__to_dto(order) for order in orders]

    def count_user_orders(self, user_id: int) -> int:
        statement = (
            select(func.count()).select_from(Order).where(Order.user_id == user_id)
        )

        return self.session.scalar(statement)

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
            items=[self.__to_order_item_model(item_dto=item) for item in dto.items],
        )

        self.session.add(order)

    def get_expired_orders(self) -> list[OrderDataDto]:
        cutoff = datetime.now(UTC) - timedelta(hours=1)

        statement = (
            select(Order)
            .where(Order.status == OrderStatus.NEW, Order.created_at < cutoff)
            .options(selectinload(Order.items))
            .order_by(Order.id)
            .with_for_update()
        )

        orders = self.session.scalars(statement).all()
        return [self.__to_dto(order) for order in orders]

    def cancel_expired_orders_during_transaction(self, ids: list[int]) -> None:
        self.session.execute(
            update(Order).where(Order.id.in_(ids)).values(status=OrderStatus.CANCELLED)
        )

    def __to_order_item_model(self, item_dto: CreateOrderItemDto) -> OrderItem:
        return OrderItem(
            product_id=item_dto.product_id,
            product_name=item_dto.product_name,
            price=item_dto.price,
            count=item_dto.count,
        )

    def __to_dto(self, order: Order) -> OrderDataDto:
        return OrderDataDto(
            id=order.id,
            user_id=order.user_id,
            status=order.status,
            user_name=order.user_name,
            user_phone_number=order.user_phone_number,
            user_email=order.user_email,
            user_city=order.user_city,
            user_address=order.user_address,
            total_price=order.total_price,
            created_at=order.created_at.isoformat(),
            items=[self.__to_order_item_dto(item) for item in order.items],
        )

    def __to_order_item_dto(self, item: OrderItem) -> OrderItemDataDto:
        return OrderItemDataDto(
            id=item.id,
            order_id=item.order_id,
            product_id=item.product_id,
            product_name=item.product_name,
            price=item.price,
            count=item.count,
        )
