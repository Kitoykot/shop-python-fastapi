from app.database.unit_of_work import UnitOfWork
from app.enums.order.order_status import OrderStatus
from app.exceptions.order.order_cancelled_status_exception import (
    OrderCancelledStatusException,
)
from app.exceptions.order.order_completed_status_exception import (
    OrderCompletedStatusException,
)
from app.exceptions.order.order_in_transit_status_exception import (
    OrderInTransitStatusException,
)
from app.exceptions.order.order_not_found_exception import OrderNotFoundException
from app.repositories.order.order_repository import OrderRepository
from app.repositories.product.product_repository import ProductRepository


class CancelOrderService:
    def __init__(
        self,
        repository: OrderRepository,
        product_repository: ProductRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.product_repository = product_repository
        self.unit_of_work = unit_of_work

    def cancel_expired_orders(self) -> None:
        with self.unit_of_work:
            orders = self.repository.get_expired_orders()

            if len(orders) == 0:
                return

            self.repository.cancel_expired_orders_during_transaction(
                [order.id for order in orders]
            )

            self.product_repository.increase_counts_during_transaction(
                [item for order in orders for item in order.items]
            )

    def cancel_order_by_user(self, order_id: int, user_id: int) -> None:
        with self.unit_of_work:
            order = self.repository.get_order_details_for_cancelling(
                order_id=order_id, user_id=user_id
            )

            if order is None:
                raise OrderNotFoundException()

            if order.status == OrderStatus.CANCELLED:
                raise OrderCancelledStatusException()

            if order.status == OrderStatus.IN_TRANSIT:
                raise OrderInTransitStatusException()

            if order.status == OrderStatus.COMPLETED:
                raise OrderCompletedStatusException()

            self.repository.cancel_order_by_user_during_transaction(
                order_id=order_id, user_id=user_id
            )

            self.product_repository.increase_counts_during_transaction(order.items)
