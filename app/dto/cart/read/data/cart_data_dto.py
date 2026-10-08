from dataclasses import dataclass

from app.dto.cart.read.data.cart_item_data_dto import CartItemDataDto


@dataclass
class CartDataDto:
    id: int
    user_id: int
    items: list[CartItemDataDto]
