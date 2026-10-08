from app.database.unit_of_work import UnitOfWork
from app.repositories.order.order_repository import OrderRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.order.cancel_order_service import CancelOrderService
from config.postgresql.connection import SessionFactory


def main() -> None:
    with SessionFactory() as session:
        CancelOrderService(
            repository=OrderRepository(session),
            product_repository=ProductRepository(session),
            unit_of_work=UnitOfWork(session),
        ).cancel_expired_orders()


if __name__ == '__main__':
    main()
