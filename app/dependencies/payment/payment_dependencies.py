from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.unit_of_work import UnitOfWork
from app.dependencies.db.db_dependency import get_db
from app.repositories.order.order_repository import OrderRepository
from app.repositories.payment.payment_repository import PaymentRepository
from app.services.payment.confirm_payment_service import ConfirmPaymentService
from app.services.payment.create_payment_service import CreatePaymentService


def get_create_payment_service(
    session: Session = Depends(get_db),
) -> CreatePaymentService:
    return CreatePaymentService(
        repository=PaymentRepository(session),
        order_repository=OrderRepository(session),
        unit_of_work=UnitOfWork(session),
    )


def get_confirm_payment_service(
    session: Session = Depends(get_db),
) -> ConfirmPaymentService:

    return ConfirmPaymentService(
        repository=PaymentRepository(session),
        order_repository=OrderRepository(session),
        unit_of_work=UnitOfWork(session),
    )
