from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.dto.payment.create.create_payment_dto import CreatePaymentDto
from app.dto.payment.read.data.payment_data_dto import PaymentDataDto
from app.enums.payment.payment_status import PaymentStatus
from app.models.payment.payment import Payment


class PaymentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_order_id_by_payment(self, payment_id: int) -> int | None:
        return self.session.scalar(
            select(Payment.order_id).where(Payment.id == payment_id)
        )

    def get_payment_for_confirmation(self, payment_id: int) -> PaymentDataDto | None:
        payment = self.session.scalar(
            select(Payment)
            .where(Payment.id == payment_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        return self.__to_dto(payment) if payment is not None else None

    def mark_succeeded_during_transaction(
        self, payment_id: int, paid_at: datetime
    ) -> None:
        self.session.execute(
            update(Payment)
            .where(Payment.id == payment_id)
            .values(status=PaymentStatus.SUCCEEDED, paid_at=paid_at)
        )

    def create_payment_during_transaction(
        self, dto: CreatePaymentDto
    ) -> PaymentDataDto:
        payment = Payment(
            order_id=dto.order_id,
            provider=dto.provider,
            status=dto.status,
            amount=dto.amount,
            currency=dto.currency,
        )

        self.session.add(payment)
        self.session.flush()

        return self.__to_dto(payment)

    def __to_dto(self, payment: Payment) -> PaymentDataDto:
        return PaymentDataDto(
            id=payment.id,
            order_id=payment.order_id,
            provider=payment.provider,
            provider_payment_id=payment.provider_payment_id,
            status=payment.status,
            amount=payment.amount,
            currency=payment.currency,
            paid_at=payment.paid_at,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
        )
