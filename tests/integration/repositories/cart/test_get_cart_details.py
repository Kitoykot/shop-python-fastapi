from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.dto.cart.data.cart_item_data_dto import CartItemDataDto
from app.dto.product.product_dto import ProductDto
from app.enums.user.user_role import UserRole
from app.models.cart.cart import Cart
from app.models.cart.cart_item import CartItem
from app.models.product.product import Product
from app.models.user.user import User
from app.repositories.cart.cart_repository import CartRepository


class TestGetCartDetails:
    @pytest.fixture(autouse=True)
    def setup_data(self, user: User, repository: CartRepository):
        self.user = user
        self.repository = repository

    def test_missing_cart(self) -> None:
        assert self.repository.get_cart_details(self.user.id) is None

    def test_not_my_cart(self, db_session: Session) -> None:
        other_user = User(
            first_name='User',
            middle_name='Userovich',
            last_name='Userov',
            email='other-user@test.com',
            password_hash='test-hash',
            phone_number='78901234576',
            is_active=True,
            role=UserRole.USER,
        )

        db_session.add(other_user)
        db_session.flush()

        cart = Cart(user_id=other_user.id)

        db_session.add(cart)
        db_session.flush()

        assert self.repository.get_cart_details(self.user.id) is None

    def test_cart_without_products(self, db_session: Session) -> None:
        cart = Cart(user_id=self.user.id)

        db_session.add(cart)
        db_session.flush()

        result = self.repository.get_cart_details(self.user.id)

        assert result is not None
        assert result.id == cart.id
        assert result.user_id == self.user.id
        assert result.items == []

    def test_cart_with_products(self, db_session: Session) -> None:
        cart = Cart(user_id=self.user.id)
        product_one = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=20,
        )
        product_two = Product(
            name='Product 2',
            description='Product 2 description',
            price=Decimal('10.50'),
            show_in_catalog=False,
            count=10,
        )

        db_session.add_all([cart, product_one, product_two])
        db_session.flush()

        cart_item_one = CartItem(cart_id=cart.id, product_id=product_one.id, count=6)
        cart_item_two = CartItem(cart_id=cart.id, product_id=product_two.id, count=7)

        db_session.add_all([cart_item_one, cart_item_two])
        db_session.flush()

        result = self.repository.get_cart_details(self.user.id)

        assert result is not None
        assert result.id == cart.id
        assert result.user_id == self.user.id
        assert result.items == [
            CartItemDataDto(
                id=cart_item_one.id,
                count=cart_item_one.count,
                product=ProductDto(
                    id=product_one.id,
                    name=product_one.name,
                    description=product_one.description,
                    price=product_one.price,
                    show_in_catalog=product_one.show_in_catalog,
                    count=product_one.count,
                    is_available=product_one.is_available,
                ),
            ),
            CartItemDataDto(
                id=cart_item_two.id,
                count=cart_item_two.count,
                product=ProductDto(
                    id=product_two.id,
                    name=product_two.name,
                    description=product_two.description,
                    price=product_two.price,
                    show_in_catalog=product_two.show_in_catalog,
                    count=product_two.count,
                    is_available=product_two.is_available,
                ),
            ),
        ]
