from pydantic import BaseModel

from app.http.responses.cart.cart_item.cart_item_response import CartItemResponse
from app.http.responses.cart.cart_response import CartResponse


class CartDetailsResponse(BaseModel):
    cart: CartResponse
    items: list[CartItemResponse]
