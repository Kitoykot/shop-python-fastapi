from dataclasses import dataclass


@dataclass
class CartItemForOrderDto:
    id: int
    cart_id: int
    count: int
    product_id: int
