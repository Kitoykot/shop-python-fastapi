from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.user.user import User
    from app.models.cart.cart_item import CartItem

class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='cart'
    )
    items: Mapped[list['CartItem']] = relationship(
        'CartItem',
        back_populates='cart',
        order_by='CartItem.id'
    )