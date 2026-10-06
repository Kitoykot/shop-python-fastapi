from fastapi import APIRouter

from app.http.controllers.api.v1.auth.auth_controller import router as auth
from app.http.controllers.api.v1.cart.cart_controller import router as cart
from app.http.controllers.api.v1.category.category_controller import (
    router as categories,
)
from app.http.controllers.api.v1.order.order_controller import router as orders
from app.http.controllers.api.v1.product.product_controller import router as products

router = APIRouter(prefix='/api/v1')

router.include_router(auth)
router.include_router(products)
router.include_router(categories)
router.include_router(cart)
router.include_router(orders)
