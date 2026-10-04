from pydantic import BaseModel

from app.http.responses.cart.cart_response import CartResponse
from app.http.responses.cart.cart_item.cart_item_response import CartItemResponse



class CartDetailsResponse(BaseModel):
    cart: CartResponse
    items: list[CartItemResponse]