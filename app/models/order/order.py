from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.order.order_status import OrderStatus
from app.models.base import Base

if TYPE_CHECKING:
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
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped['User'] = relationship('User', back_populates='orders')