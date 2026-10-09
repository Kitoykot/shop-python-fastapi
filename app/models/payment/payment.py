from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.payment.payment_status import PaymentStatus
from app.models.base import Base


class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        UniqueConstraint('provider', 'provider_payment_id', name='uq_provider_payment'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    provider: Mapped[str] = mapped_column(String(128))
    provider_payment_id: Mapped[str | None] = mapped_column(String(256))
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(
            PaymentStatus,
            name='payment_status',
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        default=PaymentStatus.PENDING,
        server_default='pending',
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(
        String(8),
        default='RUB',
        server_default='RUB',
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
