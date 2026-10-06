from fastapi import APIRouter, Depends, status

from app.dependencies.auth.current_user_dependency import get_current_user
from app.dependencies.order.order_dependencies import get_create_order_service
from app.dto.user.user_dto import UserDto
from app.http.requests.order.create_order_request import CreateOrderRequest
from app.http.responses.order.order_created_response import OrderCreatedResponse
from app.services.order.create_order_service import CreateOrderService

router = APIRouter(prefix='/orders')


@router.post('', status_code=status.HTTP_201_CREATED)
def create_order(
    request: CreateOrderRequest,
    user: UserDto = Depends(get_current_user),
    service: CreateOrderService = Depends(get_create_order_service),
) -> OrderCreatedResponse:
    service.create_order(user_id=user.id, dto=request.create_dto())

    return OrderCreatedResponse(
        code=status.HTTP_201_CREATED,
        message='Заказ успешно создан',
    )
