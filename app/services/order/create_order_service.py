from decimal import Decimal

from app.database.unit_of_work import UnitOfWork
from app.dto.cart.cart_item_for_order_dto import CartItemForOrderDto
from app.dto.order.create_order_dto import CreateOrderDto
from app.dto.order.create_order_item_dto import CreateOrderItemDto
from app.dto.order.order_create_data_dto import OrderCreateDataDto
from app.dto.product.product_dto import ProductDto
from app.exceptions.order.empty_cart_exception import EmptyCartException
from app.exceptions.order.item_count_exception import ItemCountException
from app.exceptions.order.item_is_not_available_exception import (
    ItemIsNotAvailableException,
)
from app.exceptions.order.some_items_are_not_available_exception import (
    SomeItemsAreNotAvailableException,
)
from app.repositories.cart.cart_repository import CartRepository
from app.repositories.order.order_repository import OrderRepository
from app.repositories.product.product_repository import ProductRepository


class CreateOrderService:
    def __init__(
        self,
        repository: OrderRepository,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
        unit_of_work: UnitOfWork,
    ):
        self.repository = repository
        self.cart_repository = cart_repository
        self.product_repository = product_repository
        self.unit_of_work = unit_of_work

    def create_order(self, user_id: int, dto: CreateOrderDto) -> None:
        with self.unit_of_work:
            cart = self.cart_repository.get_cart_for_order(user_id)

            if cart is None or len(cart.items) == 0:
                raise EmptyCartException()

            product_ids = [item.product_id for item in cart.items]
            products = self.product_repository.get_products_by_ids_list(product_ids)

            if set(product_ids) != {product.id for product in products}:
                raise SomeItemsAreNotAvailableException()

            self.__check_items_count_before_order(
                cart_items=cart.items, products=products
            )

            create_order_data_dto = self.__to_order_create_data_dto(
                user_id=user_id, dto=dto, cart_items=cart.items, products=products
            )

            self.repository.create_order_during_transaction(create_order_data_dto)
            self.product_repository.decrease_counts_during_transaction(cart.items)
            self.cart_repository.delete_all_cart_items_during_transaction(user_id)

    def __check_items_count_before_order(
        self,
        cart_items: list[CartItemForOrderDto],
        products: list[ProductDto],
    ) -> None:
        products_by_id = self.__get_products_dict_list(products)

        for item in cart_items:
            product = products_by_id[item.product_id]

            if product.is_available is False or product.count is None:
                raise ItemIsNotAvailableException(product.name)

            if item.count > product.count:
                raise ItemCountException(product.name)

    def __to_order_create_data_dto(
        self,
        user_id: int,
        dto: CreateOrderDto,
        products: list[ProductDto],
        cart_items: list[CartItemForOrderDto],
    ) -> OrderCreateDataDto:
        return OrderCreateDataDto(
            user_id=user_id,
            user_name=dto.user_name,
            user_phone_number=dto.user_phone_number,
            user_email=dto.user_email,
            user_city=dto.user_city,
            user_address=dto.user_address,
            total_price=self.__get_total_price(
                products=products, cart_items=cart_items
            ),
            items=self.__get_create_order_item_dtos(
                products=products, cart_items=cart_items
            ),
        )

    def __get_total_price(
        self,
        products: list[ProductDto],
        cart_items: list[CartItemForOrderDto],
    ) -> Decimal:
        total_price = Decimal('0')
        products_by_id = self.__get_products_dict_list(products)

        for item in cart_items:
            product = products_by_id[item.product_id]
            total_price += product.price * item.count

        return total_price

    def __get_create_order_item_dtos(
        self,
        products: list[ProductDto],
        cart_items: list[CartItemForOrderDto],
    ) -> list[CreateOrderItemDto]:
        products_by_id = self.__get_products_dict_list(products)
        items = []

        for item in cart_items:
            product = products_by_id[item.product_id]
            items.append(
                CreateOrderItemDto(
                    product_id=product.id,
                    product_name=product.name,
                    price=product.price,
                    count=item.count,
                )
            )

        return items

    def __get_products_dict_list(
        self, products: list[ProductDto]
    ) -> dict[int, ProductDto]:
        return {product.id: product for product in products}
