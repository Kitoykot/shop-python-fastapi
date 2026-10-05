from app.repositories.order.order_repository import OrderRepository


class CreateOrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository