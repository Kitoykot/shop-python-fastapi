from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.order.order import Order


class OrderItem(Base):
    __tablename__ = 'order_items'
    __table_args__ = (
        CheckConstraint('count > 0', name='check_order_items_count_positive'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product_name: Mapped[str] = mapped_column(String(256))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    count: Mapped[int] = mapped_column(SmallInteger)

    order: Mapped['Order'] = relationship('Order', back_populates='items')
