from dataclasses import dataclass

from app.dto.product.read.data.product_data_dto import ProductDataDto


@dataclass
class CartItemDataDto:
    id: int
    count: int
    product: ProductDataDto
