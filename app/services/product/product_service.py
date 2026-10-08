from app.dto.product.create.create_product_dto import CreateProductDto
from app.dto.product.read.data.product_data_dto import ProductDataDto
from app.dto.product.update.update_product_dto import UpdateProductDto
from app.exceptions.product.product_not_found_exception import ProductNotFoundException
from app.repositories.product.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_active_products(self) -> list[ProductDataDto]:
        return self.repository.get_active_products()

    def get_product_details(self, id: int) -> ProductDataDto:
        product = self.repository.get_product_details(id)

        if product is None:
            raise ProductNotFoundException()

        return product

    def create_product(self, dto: CreateProductDto) -> None:
        self.repository.create_product(dto)

    def update_product(self, id: int, dto: UpdateProductDto) -> None:
        product = self.get_product_details(id)

        self.repository.update_product(product.id, dto)

    def delete_product(self, id: int) -> None:
        self.repository.delete_product(id)
