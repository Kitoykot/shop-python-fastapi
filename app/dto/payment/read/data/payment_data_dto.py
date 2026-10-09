from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.enums.payment.payment_status import PaymentStatus


@dataclass
class PaymentDataDto:
    id: int
    order_id: int
    provider: str
    provider_payment_id: str | None
    status: PaymentStatus
    amount: Decimal
    currency: str
    paid_at: datetime | None
    created_at: datetime
    updated_at: datetime
