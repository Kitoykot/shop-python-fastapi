from dataclasses import dataclass


@dataclass
class CartItemForOrderDataDto:
    id: int
    cart_id: int
    count: int
    product_id: int
