from dataclasses import dataclass


@dataclass
class UpdateCartItemDto:
    product_id: int
    count: int
