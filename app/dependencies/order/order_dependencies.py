from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.unit_of_work import UnitOfWork
from app.dependencies.db.db_dependency import get_db
from app.repositories.cart.cart_repository import CartRepository
from app.repositories.order.order_repository import OrderRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.order.create_order_service import CreateOrderService


def get_create_order_service(session: Session = Depends(get_db)) -> CreateOrderService:
    return CreateOrderService(
        repository=OrderRepository(session),
        cart_repository=CartRepository(session),
        product_repository=ProductRepository(session),
        unit_of_work=UnitOfWork(session),
    )
