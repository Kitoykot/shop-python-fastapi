from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db.db_dependency import get_db
from app.repositories.order.order_repository import OrderRepository
from app.services.order.create_order_service import CreateOrderService


def get_create_order_service(session: Session = Depends(get_db)) -> CreateOrderService:
    return CreateOrderService(OrderRepository(session))