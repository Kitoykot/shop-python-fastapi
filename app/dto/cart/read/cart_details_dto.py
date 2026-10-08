from dataclasses import dataclass
from decimal import Decimal

from app.dto.cart.read.cart_dto import CartDto
from app.dto.cart.read.cart_item_dto import CartItemDto


@dataclass
class CartDetailsDto:
    cart: CartDto
    items: list[CartItemDto]

    @staticmethod
    def get_empty() -> CartDetailsDto:
        return CartDetailsDto(
            cart=CartDto(
                items_count=0,
                total_price=Decimal('0'),
            ),
            items=[],
        )
