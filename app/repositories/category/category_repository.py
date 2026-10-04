from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.dto.category.category_dto import CategoryDto
from app.dto.category.create_category_dto import CreateCategoryDto
from app.dto.category.update_category_dto import UpdateCategoryDto
from app.models.category.category import Category
from app.models.category.category_products import category_products
from app.models.product.product import Product


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_active_categories(self) -> list[CategoryDto]:
        statement = select(Category).where(Category.products.any(Product.active()))
        categories = list(self.session.scalars(statement).all())

        return [self.__to_dto(category) for category in categories]

    def get_category_details(self, id: int) -> CategoryDto | None:
        statement = select(Category).where(Category.id == id)

        category = self.session.scalars(statement).first()

        if category is None:
            return None

        return self.__to_dto(category)

    def create_category(self, dto: CreateCategoryDto) -> None:
        self.session.add(Category(name=dto.name))
        self.session.commit()

    def update_category(self, id: int, dto: UpdateCategoryDto) -> None:
        statement = update(Category).where(Category.id == id).values(name=dto.name)

        self.session.execute(statement)
        self.session.commit()

    def delete_category(self, id: int) -> None:
        statement = delete(Category).where(Category.id == id)

        self.session.execute(statement)
        self.session.commit()

    def attach_product(self, category_id: int, product_id: int) -> None:
        statement = (
            insert(category_products)
            .values(category_id=category_id, product_id=product_id)
            .on_conflict_do_nothing(index_elements=['category_id', 'product_id'])
        )

        self.session.execute(statement)
        self.session.commit()

    def detach_product(self, category_id: int, product_id: int) -> None:
        statement = delete(category_products).where(
            category_products.columns.category_id == category_id,
            category_products.columns.product_id == product_id,
        )

        self.session.execute(statement)
        self.session.commit()

    def __to_dto(self, category: Category) -> CategoryDto:
        return CategoryDto(
            id=category.id,
            name=category.name,
        )
