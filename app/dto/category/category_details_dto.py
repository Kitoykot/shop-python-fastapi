from dataclasses import dataclass

from app.dto.category.category_dto import CategoryDto
from app.dto.product.product_dto import ProductDto


@dataclass
class CategoryDetailsDto:
    category: CategoryDto
    products: list[ProductDto]