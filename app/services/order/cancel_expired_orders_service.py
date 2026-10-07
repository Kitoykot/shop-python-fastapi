from app.database.unit_of_work import UnitOfWork
from app.repositories.order.order_repository import OrderRepository
from app.repositories.product.product_repository import ProductRepository


class CancelExpiredOrdersService:
    def __init__(
        self, 
        repository: OrderRepository,
        product_repository: ProductRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.product_repository = product_repository
        self.unit_of_work = unit_of_work


    def cancel_orders(self) -> None:
        with self.unit_of_work:
            orders = self.repository.get_expired_orders()

            if len(orders) == 0:
                return

            self.repository.cancel_expired_orders_during_transaction([
                order.id 
                for order in orders
            ])

            self.product_repository.increase_counts_during_transaction([
                item
                for order in orders
                for item in order.items
            ])