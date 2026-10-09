from datetime import UTC, datetime

from app.database.unit_of_work import UnitOfWork
from app.dto.order.read.data.order_data_dto import OrderDataDto
from app.dto.payment.read.data.payment_data_dto import PaymentDataDto
from app.enums.order.order_status import OrderStatus
from app.enums.payment.payment_status import PaymentStatus
from app.exceptions.payment.order_cannot_be_paid_exception import (
    OrderCannotBePaidException,
)
from app.exceptions.payment.payment_cannot_be_confirmed_exception import (
    PaymentCannotBeConfirmedException,
)
from app.exceptions.payment.payment_not_found_exception import PaymentNotFoundException
from app.repositories.order.order_repository import OrderRepository
from app.repositories.payment.payment_repository import PaymentRepository


class ConfirmPaymentService:
    def __init__(
        self,
        repository: PaymentRepository,
        order_repository: OrderRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.order_repository = order_repository
        self.unit_of_work = unit_of_work

    def confirm_payment(self, payment_id: int, user_id: int) -> None:
        with self.unit_of_work:
            order_id = self.repository.get_order_id_by_payment(payment_id)
            if order_id is None:
                raise PaymentNotFoundException()

            order = self.order_repository.get_order_details_for_payment(
                order_id=order_id, user_id=user_id
            )

            if order is None:
                raise PaymentNotFoundException()

            payment = self.repository.get_payment_for_confirmation(payment_id)

            if payment is None:
                raise PaymentNotFoundException()

            if self.__check_payment(payment, order) is False:
                return

            self.repository.mark_succeeded_during_transaction(
                payment_id=payment.id, paid_at=datetime.now(UTC)
            )
            self.order_repository.mark_paid_during_transaction(order.id)

    def __check_payment(self, payment: PaymentDataDto, order: OrderDataDto) -> bool:
        if payment.status == PaymentStatus.SUCCEEDED:
            return False

        if order.status != OrderStatus.NEW:
            raise OrderCannotBePaidException()

        if (
            payment.status != PaymentStatus.PENDING
            or payment.amount != order.total_price
        ):
            raise PaymentCannotBeConfirmedException()

        return True
