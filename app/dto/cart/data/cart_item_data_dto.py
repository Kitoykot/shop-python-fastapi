from dataclasses import dataclass

from app.dto.product.product_dto import ProductDto


@dataclass
class CartItemDataDto:
    id: int
    count: int
    product: ProductDto
