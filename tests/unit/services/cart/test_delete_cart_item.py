from unittest.mock import Mock

from app.repositories.cart.cart_repository import CartRepository
from app.repositories.product.product_repository import ProductRepository
from app.services.cart.cart_service import CartService


class TestDeleteCartItem:
    def setup_method(self):
        self.cart_repository = Mock(spec=CartRepository)
        self.product_repository = Mock(spec=ProductRepository)

        self.service = CartService(
            repository=self.cart_repository,
            product_repository=self.product_repository
        )


    def test_success_delete_cart_item(self) -> None:
        self.service.delete_cart_item(item_id=1, user_id=2)

        self.cart_repository.delete_cart_item.assert_called_once_with(item_id=1, user_id=2)