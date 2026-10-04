from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db.db_dependency import get_db
from app.repositories.cart.cart_repository import CartRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.cart.cart_service import CartService


def get_cart_service(session: Session = Depends(get_db)) -> CartService:
    return CartService(
        CartRepository(session),
        ProductRepository(session),
    )
