from dataclasses import dataclass

from app.dto.cart.read.data.cart_item_for_order_data_dto import CartItemForOrderDataDto


@dataclass
class CartForOrderDataDto:
    id: int
    user_id: int
    items: list[CartItemForOrderDataDto]
