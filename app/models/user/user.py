from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.user.user_role import UserRole
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.cart.cart import Cart
    from app.models.order.order import Order


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64))
    middle_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    phone_number: Mapped[str] = mapped_column(String(16), unique=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default='true'
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name='user_role',
            values_callable=lambda roles: [role.value for role in roles],
        ),
        default=UserRole.USER,
        server_default='user',
    )

    cart: Mapped['Cart | None'] = relationship(
        'Cart',
        back_populates='user',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')
