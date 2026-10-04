from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, UniqueConstraint

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.cart.cart import Cart
    from app.models.product.product import Product

class CartItem(Base):
    __tablename__ = 'cart_items'
    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id'),
        CheckConstraint('count > 0', name='check_cart_items_count_positive')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(
        ForeignKey('carts.id', ondelete='CASCADE'),
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'),
    )
    count: Mapped[int] = mapped_column(
        SmallInteger, 
        default=1, 
        server_default="1"
    )

    cart: Mapped['Cart'] = relationship(
        'Cart',
        back_populates='items'
    )
    product: Mapped['Product'] = relationship('Product')
