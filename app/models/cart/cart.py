from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.cart.cart_item import CartItem
    from app.models.user.user import User


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
    )

    user: Mapped['User'] = relationship('User', back_populates='cart')
    items: Mapped[list['CartItem']] = relationship(
        'CartItem',
        back_populates='cart',
        order_by='CartItem.id',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
