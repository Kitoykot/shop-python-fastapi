from sqlalchemy import select, delete, update

from app.models.product.product import Product
from app.dto.product.product_dto import ProductDto
from app.dto.product.create_product_dto import CreateProductDto
from app.dto.product.update_product_dto import UpdateProductDto
from sqlalchemy.orm import Session


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_active_products(self) -> list[ProductDto]:
        statement = select(Product).where(Product.active())

        products = list(self.session.scalars(statement).all())

        return [self.__to_dto(product) for product in products]

    def get_products_by_category(self, category_id: int) -> list[ProductDto]:
        statement = (
            select(Product)
            .where(
                Product.categories.any(id=category_id),
                Product.active()
            )
            .order_by(Product.id)
        )

        products = self.session.scalars(statement).all()

        return [
            self.__to_dto(product)
            for product in products
        ]

    def get_product_details(self, id: int) -> ProductDto | None:
        statement = select(Product).where(Product.id == (id))

        product = self.session.scalars(statement).first()

        if product is None:
            return None

        return self.__to_dto(product)

    def create_product(self, dto: CreateProductDto) -> None:
        product = Product(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            count=dto.count,
        )

        self.session.add(product)
        self.session.commit()

    def update_product(self, id: int, dto: UpdateProductDto) -> None:
        statement = update(Product).where(Product.id == id).values(**dto.fields)

        self.session.execute(statement)
        self.session.commit()

    def delete_product(self, id: int) -> None:
        statement = delete(Product).where(Product.id == id)

        self.session.execute(statement)
        self.session.commit()

    def __to_dto(self, product: Product) -> ProductDto:
        return ProductDto(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            show_in_catalog=product.show_in_catalog,
            count=product.count,
            is_available=product.is_available
        )
