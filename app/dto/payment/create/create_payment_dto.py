from dataclasses import dataclass
from decimal import Decimal

from app.enums.payment.payment_status import PaymentStatus


@dataclass
class CreatePaymentDto:
    order_id: int
    provider: str
    status: PaymentStatus
    amount: Decimal
    currency: str
