from decimal import Decimal

from app.dto.cart.cart_details_dto import CartDetailsDto
from app.dto.cart.cart_dto import CartDto
from app.dto.cart.cart_item_dto import CartItemDto
from app.dto.cart.data.cart_data_dto import CartDataDto
from app.dto.cart.data.cart_item_data_dto import CartItemDataDto
from app.dto.cart.update_cart_item_dto import UpdateCartItemDto

from app.exceptions.product.product_not_found_exception import ProductNotFoundException
from app.models.cart.cart import Cart
from app.repositories.cart.cart_repository import CartRepository
from app.repositories.product.product_repository import ProductRepository


class CartService:
    def __init__(
        self, 
        repository: CartRepository,
        product_repository: ProductRepository,
    ):
        self.repository = repository
        self.product_repository = product_repository


    def get_cart(self, user_id: int) -> CartDetailsDto:
        cart = self.repository.get_cart_details(user_id)
    
        if cart is None:
            return CartDetailsDto.get_empty()

        return self.__process_cart(cart)


    def update_cart_item(self, user_id: int, dto: UpdateCartItemDto):
        product = self.product_repository.get_product_details(dto.product_id)

        if product is None or product.is_available is False:
            raise ProductNotFoundException()

        self.repository.update_cart_item(user_id=user_id, dto=dto)


    def delete_cart_item(self, item_id: int, user_id: int) -> None:
        self.repository.delete_cart_item(item_id=item_id, user_id=user_id)
        

    def clear_cart(self, user_id: int) -> None:
        self.repository.delete_all_cart_items(user_id)


    def __process_cart(self, cart: CartDataDto) -> CartDetailsDto:
        available_items = [
            item
            for item in cart.items
            if self.__get_is_available(item)
        ]

        return CartDetailsDto(
            cart=CartDto(
                items_count=sum(item.count for item in available_items),
                total_price=self.__get_total_sum(available_items)
            ),
            items=[
                self.__to_cart_item_dto(item)
                for item in cart.items
            ]
        )

    def __get_total_sum(self, available_items: list[CartItemDataDto]) -> Decimal:        
        total_price = Decimal('0')

        for item in available_items:
            total_price += item.count * item.product.price

        return total_price

    
    def __to_cart_item_dto(self, item: CartItemDataDto) -> CartItemDto:
        return CartItemDto(
                id=item.id,
                product_id=item.product.id,
                name=item.product.name,
                count=item.count,
                price=item.product.price,
                is_available=self.__get_is_available(item),
            )
    

    def __get_is_available(self, item: CartItemDataDto) -> bool:
        if item.product.count is None:
            return False

        if item.count <= item.product.count and item.product.is_available is True:
            return True

        return False