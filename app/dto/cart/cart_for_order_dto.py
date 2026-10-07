from dataclasses import dataclass

from app.dto.cart.cart_item_for_order_dto import CartItemForOrderDto


@dataclass
class CartForOrderDto:
    id: int
    user_id: int
    items: list[CartItemForOrderDto]
