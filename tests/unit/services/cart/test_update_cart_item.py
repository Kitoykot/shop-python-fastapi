from decimal import Decimal
from unittest.mock import Mock

import pytest

from app.dto.cart.update_cart_item_dto import UpdateCartItemDto
from app.dto.product.product_dto import ProductDto
from app.exceptions.product.product_not_found_exception import ProductNotFoundException
from app.repositories.cart.cart_repository import CartRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.cart.cart_service import CartService


class TestUpdateCartItem:
    def setup_method(self):
        self.cart_repository = Mock(spec=CartRepository)
        self.product_repository = Mock(spec=ProductRepository)

        self.service = CartService(
            repository=self.cart_repository,
            product_repository=self.product_repository
        )


    def test_if_product_is_none(self) -> None:
        self.product_repository.get_product_details.return_value = None
        dto = UpdateCartItemDto(
            product_id=1,
            count=2,
        )

        with pytest.raises(ProductNotFoundException):
            self.service.update_cart_item(user_id=3, dto=dto)

        self.cart_repository.update_cart_item.assert_not_called()

    def test_if_product_is_not_active(self) -> None:
        self.product_repository.get_product_details.return_value = ProductDto(
            id=1,
            name='Product 1',
            description='',
            price=Decimal('10.50'),
            show_in_catalog=False,
            count=10,
            is_available=False,
        )

        dto = UpdateCartItemDto(
            product_id=1,
            count=3,
        )

        with pytest.raises(ProductNotFoundException):
            self.service.update_cart_item(user_id=4, dto=dto)

        self.cart_repository.update_cart_item.assert_not_called()


    def test_success_update(self) -> None:
        self.product_repository.get_product_details.return_value = ProductDto(
            id=1,
            name='Product 1',
            description='',
            price=Decimal('10.50'),
            show_in_catalog=True,
            count=10,
            is_available=True,
        )

        dto = UpdateCartItemDto(
            product_id=1,
            count=3,
        )

        self.service.update_cart_item(user_id=4, dto=dto)

        self.product_repository.get_product_details.assert_called_once_with(1)
        self.cart_repository.update_cart_item.assert_called_once_with(user_id=4, dto=dto)


    def test_success_update_if_request_count_is_bigger(self) -> None:
        self.product_repository.get_product_details.return_value = ProductDto(
            id=1,
            name='Product 1',
            description='',
            price=Decimal('10.50'),
            show_in_catalog=True,
            count=2,
            is_available=True,
        )

        dto = UpdateCartItemDto(
            product_id=1,
            count=3,
        )

        self.service.update_cart_item(user_id=4, dto=dto)

        self.product_repository.get_product_details.assert_called_once_with(1)
        self.cart_repository.update_cart_item.assert_called_once_with(user_id=4, dto=dto)
        