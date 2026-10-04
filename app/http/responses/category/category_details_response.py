from pydantic import BaseModel

from app.http.responses.category.category_response import CategoryResponse
from app.http.responses.product.product_list_response import ProductListResponse


class CategoryDetailsResponse(BaseModel):
    category: CategoryResponse
    products: list[ProductListResponse]
