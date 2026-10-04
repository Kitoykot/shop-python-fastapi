from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.user.user_role import UserRole
from app.models.cart.cart import Cart
from app.models.cart.cart_item import CartItem
from app.models.product.product import Product
from app.models.user.user import User
from app.repositories.cart.cart_repository import CartRepository


class TestDeleteCartItem:
    @pytest.fixture(autouse=True)
    def setup_data(self, user: User, repository: CartRepository):
        self.user = user
        self.repository = repository

    def test_cart_id_is_none(self, db_session: Session) -> None:
        self.repository.delete_cart_item(item_id=1, user_id=self.user.id)

        statement = select(Cart).where(Cart.user_id == self.user.id)
        assert db_session.scalar(statement) is None

    def test_delete_cart_item(self, db_session: Session) -> None:
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
            show_in_catalog=True,
            count=10,
        )

        db_session.add_all([cart, product_one, product_two])
        db_session.flush()

        cart_item_one = CartItem(
            cart_id=cart.id,
            product_id=product_one.id,
            count=6,
        )
        cart_item_two = CartItem(
            cart_id=cart.id,
            product_id=product_two.id,
            count=7,
        )

        db_session.add_all([cart_item_one, cart_item_two])
        db_session.flush()

        self.repository.delete_cart_item(item_id=cart_item_one.id, user_id=self.user.id)

        statement = select(CartItem.id).where(CartItem.cart_id == cart.id)
        cart_item_ids = db_session.scalars(statement).all()

        assert cart is not None
        assert cart_item_ids == [cart_item_two.id]

    def test_delete_cart_item_if_no_item(self, db_session: Session) -> None:
        cart = Cart(user_id=self.user.id)

        db_session.add(cart)
        db_session.flush()

        self.repository.delete_cart_item(item_id=1, user_id=self.user.id)

        cart_statement = select(Cart).where(Cart.user_id == self.user.id)
        existing_cart = db_session.execute(cart_statement).scalar_one()

        assert existing_cart is not None
        assert existing_cart.id == cart.id

    def test_delete_only_my_cart_item(self, db_session: Session) -> None:
        user_two = User(
            first_name='User 1',
            middle_name='Userovich 2',
            last_name='Userov 3',
            email='user-two@test.com',
            password_hash='test-hash-two',
            phone_number='78901234576',
            is_active=True,
            role=UserRole.USER,
        )

        db_session.add(user_two)
        db_session.flush()

        cart_one = Cart(user_id=self.user.id)
        cart_two = Cart(user_id=user_two.id)

        db_session.add_all([cart_one, cart_two])
        db_session.flush()

        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=20,
        )

        db_session.add(product)
        db_session.flush()

        cart_item_one = CartItem(
            cart_id=cart_one.id,
            product_id=product.id,
            count=6,
        )
        cart_item_two = CartItem(
            cart_id=cart_two.id,
            product_id=product.id,
            count=7,
        )

        db_session.add_all([cart_item_one, cart_item_two])
        db_session.flush()

        self.repository.delete_cart_item(item_id=cart_item_one.id, user_id=self.user.id)

        statement = select(CartItem).where(CartItem.cart_id == cart_one.id)
        my_cart_item = db_session.scalar(statement)

        other_user_cart_item_statement = select(CartItem).where(
            CartItem.cart_id == cart_two.id
        )
        other_user_cart_item = db_session.execute(
            other_user_cart_item_statement
        ).scalar_one()

        assert my_cart_item is None
        assert other_user_cart_item is not None
        assert other_user_cart_item.cart_id == cart_two.id

    def test_cant_delete_other_user_cart_item(self, db_session: Session) -> None:
        user_two = User(
            first_name='User 2',
            middle_name=None,
            last_name='Userov',
            email='user-two@test.com',
            password_hash='test-hash-two',
            phone_number='78901234576',
            is_active=True,
            role=UserRole.USER,
        )
        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=20,
        )
        db_session.add_all([user_two, product])
        db_session.flush()

        cart_one = Cart(user_id=self.user.id)
        cart_two = Cart(user_id=user_two.id)
        db_session.add_all([cart_one, cart_two])
        db_session.flush()

        cart_item_one = CartItem(
            cart_id=cart_one.id,
            product_id=product.id,
            count=6,
        )
        cart_item_two = CartItem(
            cart_id=cart_two.id,
            product_id=product.id,
            count=7,
        )
        db_session.add_all([cart_item_one, cart_item_two])
        db_session.flush()

        cart_ids = [cart_one.id, cart_two.id]
        expected_item_ids = {cart_item_one.id, cart_item_two.id}

        self.repository.delete_cart_item(
            item_id=cart_item_two.id,
            user_id=self.user.id,
        )

        statement = select(CartItem.id).where(CartItem.cart_id.in_(cart_ids))
        remaining_item_ids = db_session.scalars(statement).all()

        assert set(remaining_item_ids) == expected_item_ids
