from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dto.cart.update_cart_item_dto import UpdateCartItemDto
from app.models.cart.cart import Cart
from app.models.cart.cart_item import CartItem
from app.models.product.product import Product
from app.models.user.user import User
from app.repositories.cart.cart_repository import CartRepository


class TestUpdateCartItem:
    @pytest.fixture(autouse=True)
    def setup_data(self, user: User, repository: CartRepository, db_session: Session):
        self.user = user
        self.repository = repository

        self.product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=20,
        )

        db_session.add(self.product)
        db_session.flush()

    def test_add_item(self, db_session: Session) -> None:
        cart = Cart(user_id=self.user.id)

        db_session.add(cart)
        db_session.flush()

        self.repository.update_cart_item(
            user_id=self.user.id,
            dto=UpdateCartItemDto(product_id=self.product.id, count=2),
        )

        cart_item_statement = select(CartItem).where(CartItem.cart_id == cart.id)
        result = db_session.scalar(cart_item_statement)

        assert result is not None
        assert result.cart_id == cart.id
        assert result.product_id == self.product.id
        assert result.count == 2

    def test_add_item_if_cart_not_exists(self, db_session: Session) -> None:
        self.repository.update_cart_item(
            user_id=self.user.id,
            dto=UpdateCartItemDto(product_id=self.product.id, count=4),
        )

        cart_statement = select(Cart).where(Cart.user_id == self.user.id)
        cart = db_session.scalar(cart_statement)

        assert cart is not None
        assert cart.user_id == self.user.id

        cart_item_statement = select(CartItem).where(CartItem.cart_id == cart.id)
        result = db_session.scalar(cart_item_statement)

        assert result is not None
        assert result.cart_id == cart.id
        assert result.product_id == self.product.id
        assert result.count == 4

    def test_update_item(self, db_session: Session) -> None:
        cart = Cart(user_id=self.user.id)

        db_session.add(cart)
        db_session.flush()

        cart_item = CartItem(cart_id=cart.id, product_id=self.product.id, count=2)
        db_session.add(cart_item)
        db_session.flush()

        self.repository.update_cart_item(
            user_id=self.user.id,
            dto=UpdateCartItemDto(product_id=self.product.id, count=4),
        )

        cart_item_statement = select(CartItem).where(CartItem.cart_id == cart.id)
        result = db_session.execute(cart_item_statement).scalar_one()

        assert result is not None
        assert result.id == cart_item.id
        assert result.cart_id == cart.id
        assert result.product_id == self.product.id
        assert result.count == 4
