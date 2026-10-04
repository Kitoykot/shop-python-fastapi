from typing import TYPE_CHECKING

from sqlalchemy import String

from app.models.base import Base
from app.models.category.category_products import category_products
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.product.product import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))

    products: Mapped[list["Product"]] = relationship(
        "Product", 
        secondary=category_products, 
        back_populates="categories",
    )
