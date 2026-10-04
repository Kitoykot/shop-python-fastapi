from fastapi import APIRouter, Depends, status

from app.dependencies.auth.current_user_dependency import get_current_user
from app.dependencies.cart.cart_dependencies import get_cart_service
from app.dto.user.user_dto import UserDto
from app.http.requests.cart.cart_item.update_cart_item_request import (
    UpdateCartItemRequest,
)
from app.http.responses.cart.cart_cleared_response import CartClearedResponse
from app.http.responses.cart.cart_details_response import CartDetailsResponse
from app.http.responses.cart.cart_item.cart_item_deleted_response import (
    CartItemDeletedResponse,
)
from app.http.responses.cart.cart_item.cart_item_updated_response import (
    CartItemUpdatedResponse,
)
from app.services.cart.cart_service import CartService

router = APIRouter(prefix='/cart')


@router.get('')
def cart(
    user: UserDto = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartDetailsResponse:

    return CartDetailsResponse.model_validate(
        service.get_cart(user.id), from_attributes=True
    )


@router.post('/items')
def update_items(
    request: UpdateCartItemRequest,
    user: UserDto = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartItemUpdatedResponse:
    service.update_cart_item(user_id=user.id, dto=request.to_dto())

    return CartItemUpdatedResponse(
        code=status.HTTP_200_OK,
        message='Товар добавлен в корзину',
    )


@router.delete('/items/{item_id}')
def delete_item(
    item_id: int,
    user: UserDto = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartItemDeletedResponse:
    service.delete_cart_item(item_id=item_id, user_id=user.id)

    return CartItemDeletedResponse(
        code=status.HTTP_200_OK,
        message='Товар удален',
    )


@router.delete('/items')
def clear_cart(
    user: UserDto = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> CartClearedResponse:
    service.clear_cart(user.id)

    return CartClearedResponse(
        code=status.HTTP_200_OK,
        message='Корзина очищена',
    )
