
from app.dto.category.category_details_dto import CategoryDetailsDto
from app.dto.category.category_dto import CategoryDto
from app.dto.category.create_category_dto import CreateCategoryDto
from app.dto.category.update_category_dto import UpdateCategoryDto

from app.exceptions.category.category_not_found_exception import CategoryNotFoundException
from app.exceptions.product.product_not_found_exception import ProductNotFoundException

from app.repositories.category.category_repository import CategoryRepository
from app.repositories.product.product_repository import ProductRepository


class CategoryService:
    def __init__(
        self, 
        repository: CategoryRepository, 
        product_repository: ProductRepository
    ):
        self.repository = repository
        self.product_repository = product_repository

    def get_active_categories(self) -> list[CategoryDto]:
        return self.repository.get_active_categories()

    def get_category_details(self, id: int) -> CategoryDetailsDto:
        category = self.repository.get_category_details(id)

        if category is None:
            raise CategoryNotFoundException()

        products = self.product_repository.get_products_by_category(id)

        return CategoryDetailsDto(
            category=category,
            products=products,
        )

    def create_category(self, dto: CreateCategoryDto) -> None:
        self.repository.create_category(dto)

    def update_category(self, id: int, dto: UpdateCategoryDto) -> None:
        self.repository.update_category(id=id, dto=dto)

    def delete_category(self, id: int) -> None:
        self.repository.delete_category(id)

    def attach_product(self, category_id: int, product_id: int) -> None:
        self.get_category_details(category_id)
        product = self.product_repository.get_product_details(product_id)

        if product is None:
            raise ProductNotFoundException()

        self.repository.attach_product(category_id=category_id, product_id=product_id)

    def detach_product(self, category_id: int, product_id: int) -> None:
        self.repository.detach_product(category_id=category_id, product_id=product_id)
