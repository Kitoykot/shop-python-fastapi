from app.database.unit_of_work import UnitOfWork
from app.repositories.order.order_repository import OrderRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.order.cancel_expired_orders_service import CancelExpiredOrdersService
from config.postgresql.connection import SessionFactory


def main() -> None:
    with SessionFactory() as session:
        CancelExpiredOrdersService(
            repository=OrderRepository(session),
            product_repository=ProductRepository(session),
            unit_of_work=UnitOfWork(session),
        ).cancel_orders()


if __name__ == '__main__':
    main()
