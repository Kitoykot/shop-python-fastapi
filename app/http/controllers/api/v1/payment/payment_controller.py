from fastapi import APIRouter, Depends, Path, status

from app.dependencies.auth.current_user_dependency import get_current_user
from app.dependencies.payment.payment_dependencies import (
    get_confirm_payment_service,
    get_create_payment_service,
)
from app.dto.user.read.data.user_data_dto import UserDataDto
from app.http.responses.payment.payment_confirmed_response import (
    PaymentConfirmedResponse,
)
from app.http.responses.payment.payment_created_response import PaymentCreatedResponse
from app.services.payment.confirm_payment_service import ConfirmPaymentService
from app.services.payment.create_payment_service import CreatePaymentService

router = APIRouter()


@router.post('/orders/{order_id}/payments', status_code=status.HTTP_201_CREATED)
def create_payment(
    order_id: int = Path(gt=0),
    user: UserDataDto = Depends(get_current_user),
    service: CreatePaymentService = Depends(get_create_payment_service),
) -> PaymentCreatedResponse:

    return PaymentCreatedResponse.model_validate(
        service.create_payment(order_id=order_id, user_id=user.id), from_attributes=True
    )


@router.post('/payments/{payment_id}/confirm')
def confirm_payment(
    payment_id: int = Path(gt=0),
    user: UserDataDto = Depends(get_current_user),
    service: ConfirmPaymentService = Depends(get_confirm_payment_service),
) -> PaymentConfirmedResponse:
    service.confirm_payment(payment_id=payment_id, user_id=user.id)

    return PaymentConfirmedResponse(
        code=status.HTTP_200_OK,
        message='Оплата успешно подтверждена',
    )
