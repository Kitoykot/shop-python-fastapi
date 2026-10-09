from app.database.unit_of_work import UnitOfWork
from app.dto.payment.create.create_payment_dto import CreatePaymentDto
from app.dto.payment.read.data.payment_data_dto import PaymentDataDto
from app.enums.order.order_status import OrderStatus
from app.enums.payment.payment_status import PaymentStatus
from app.exceptions.order.order_not_found_exception import OrderNotFoundException
from app.exceptions.payment.order_cannot_be_paid_exception import (
    OrderCannotBePaidException,
)
from app.repositories.order.order_repository import OrderRepository
from app.repositories.payment.payment_repository import PaymentRepository


class CreatePaymentService:
    def __init__(
        self,
        repository: PaymentRepository,
        order_repository: OrderRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.order_repository = order_repository
        self.unit_of_work = unit_of_work

    def create_payment(self, order_id: int, user_id: int) -> PaymentDataDto:
        with self.unit_of_work:
            order = self.order_repository.get_order_details_for_payment(
                order_id=order_id,
                user_id=user_id,
            )

            if order is None:
                raise OrderNotFoundException()

            if order.status != OrderStatus.NEW:
                raise OrderCannotBePaidException()

            return self.repository.create_payment_during_transaction(
                CreatePaymentDto(
                    order_id=order.id,
                    provider='fake',
                    status=PaymentStatus.PENDING,
                    amount=order.total_price,
                    currency='RUB',
                )
            )
