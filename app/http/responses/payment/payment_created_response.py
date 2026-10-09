from datetime import datetime

from pydantic import BaseModel

from app.enums.payment.payment_status import PaymentStatus
from app.http.responses.types import Price


class PaymentCreatedResponse(BaseModel):
    id: int
    order_id: int
    provider: str
    status: PaymentStatus
    amount: Price
    currency: str
    created_at: datetime
