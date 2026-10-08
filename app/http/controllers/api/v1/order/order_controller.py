from fastapi import APIRouter, Depends, Query, status

from app.dependencies.auth.current_user_dependency import get_current_user
from app.dependencies.order.order_dependencies import (
    get_create_order_service,
    get_getting_order_service,
)
from app.dto.user.read.data.user_data_dto import UserDataDto
from app.http.requests.order.create_order_request import CreateOrderRequest
from app.http.responses.order.order_created_response import OrderCreatedResponse
from app.http.responses.order.order_list_response import OrderListResponse
from app.services.order.create_order_service import CreateOrderService
from app.services.order.get_order_service import GetOrderService

router = APIRouter(prefix='/orders')


@router.post('', status_code=status.HTTP_201_CREATED)
def create_order(
    request: CreateOrderRequest,
    user: UserDataDto = Depends(get_current_user),
    service: CreateOrderService = Depends(get_create_order_service),
) -> OrderCreatedResponse:
    service.create_order(user_id=user.id, dto=request.create_dto())

    return OrderCreatedResponse(
        code=status.HTTP_201_CREATED,
        message='Заказ успешно создан',
    )


@router.get('')
def order_list(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=1, ge=1),
    user: UserDataDto = Depends(get_current_user),
    service: GetOrderService = Depends(get_getting_order_service),
) -> OrderListResponse:
    orders, pagination = service.get_order_list(
        user_id=user.id,
        page=page,
        per_page=per_page,
    )

    return OrderListResponse.model_validate(
        {'orders': orders, 'pagination': pagination},
        from_attributes=True,
    )
