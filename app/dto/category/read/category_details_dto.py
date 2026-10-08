from dataclasses import dataclass

from app.dto.category.read.data.category_data_dto import CategoryDataDto
from app.dto.product.read.data.product_data_dto import ProductDataDto


@dataclass
class CategoryDetailsDto:
    category: CategoryDataDto
    products: list[ProductDataDto]
