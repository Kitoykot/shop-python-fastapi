from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.order.order_status import OrderStatus
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.order.order_item import OrderItem
    from app.models.user.user import User


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(
            OrderStatus,
            name='order_status',
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        default=OrderStatus.NEW,
        server_default='new',
    )
    user_name: Mapped[str] = mapped_column(String(128))
    user_phone_number: Mapped[str] = mapped_column(String(16))
    user_email: Mapped[str] = mapped_column(String(254), nullable=True)
    user_city: Mapped[str] = mapped_column(String(255))
    user_address: Mapped[str] = mapped_column(String(500))
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped['User'] = relationship('User', back_populates='orders')
    items: Mapped[list['OrderItem']] = relationship(
        'OrderItem',
        back_populates='order',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )
