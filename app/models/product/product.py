from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Numeric, SmallInteger, String, Text, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.category.category_products import category_products

if TYPE_CHECKING:
    from app.models.category.category import Category


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    show_in_catalog: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default='false'
    )
    count: Mapped[int | None] = mapped_column(
        SmallInteger, default=0, server_default='0'
    )

    categories: Mapped[list['Category']] = relationship(
        'Category', secondary=category_products, back_populates='products'
    )

    @property
    def is_available(self) -> bool:
        return self.count is not None and self.count > 0 and self.show_in_catalog

    @classmethod
    def active(cls):
        return and_(cls.count > 0, cls.show_in_catalog.is_(True))
