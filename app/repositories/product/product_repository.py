from sqlalchemy import Integer, column, delete, select, update, values
from sqlalchemy.orm import Session

from app.dto.cart.cart_item_for_order_dto import CartItemForOrderDto
from app.dto.product.create_product_dto import CreateProductDto
from app.dto.product.product_dto import ProductDto
from app.dto.product.update_product_dto import UpdateProductDto
from app.models.product.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_active_products(self) -> list[ProductDto]:
        statement = select(Product).where(Product.active())
        products = self.session.scalars(statement).all()

        return [self.__to_dto(product) for product in products]

    def get_products_by_category(self, category_id: int) -> list[ProductDto]:
        statement = (
            select(Product)
            .where(Product.categories.any(id=category_id), Product.active())
            .order_by(Product.id)
        )

        products = self.session.scalars(statement).all()

        return [self.__to_dto(product) for product in products]

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


    def get_products_by_ids_list(self, product_ids: list[int]) -> list[ProductDto]:
        products = self.session.scalars(
            select(Product)
            .where(Product.id.in_(product_ids))
            .order_by(Product.id)
            .with_for_update()
        ).all()

        return [self.__to_dto(product) for product in products]


    def decrease_counts_during_transaction(self, items: list[CartItemForOrderDto]) -> None:
        if len(items) == 0:
            return
        
        ordered = values(
            column('product_id', Integer),
            column('count', Integer),
            name='ordered',
        ).data([
            (item.product_id, item.count)
            for item in items
        ])

        self.session.execute(
            update(Product)
            .where(Product.id == ordered.columns.product_id)
            .values(count=Product.count - ordered.columns.count)
        )
    

    def __to_dto(self, product: Product) -> ProductDto:
        return ProductDto(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            show_in_catalog=product.show_in_catalog,
            count=product.count,
            is_available=product.is_available,
        )
