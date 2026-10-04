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


class TestClearCart:
    @pytest.fixture(autouse=True)
    def setup_data(self, user: User, repository: CartRepository):
        self.user = user
        self.repository = repository

    def test_no_cart(self, db_session: Session) -> None:
        self.repository.delete_all_cart_items(self.user.id)

        statement = select(Cart).where(Cart.user_id == self.user.id)
        assert db_session.scalar(statement) is None

    def test_empty_cart(self, db_session: Session) -> None:
        cart = Cart(user_id=self.user.id)

        db_session.add(cart)
        db_session.flush()

        self.repository.delete_all_cart_items(self.user.id)

        cart_statement = select(Cart.id).where(Cart.user_id == self.user.id)
        items_statement = select(CartItem.id).where(CartItem.cart_id == cart.id)

        assert db_session.scalar(cart_statement) == cart.id
        assert db_session.scalars(items_statement).all() == []

    def test_with_items_in_cart(self, db_session: Session) -> None:
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

        self.repository.delete_all_cart_items(self.user.id)

        product_ids = [product_one.id, product_two.id]

        cart_statement = select(Cart.id).where(
            Cart.user_id == self.user.id, Cart.id == cart.id
        )
        remaining_cart_items_ids_statement = select(CartItem.id).where(
            CartItem.cart_id == cart.id
        )
        product_ids_statement = select(Product.id).where(Product.id.in_(product_ids))

        assert db_session.execute(cart_statement).scalar_one() is not None
        assert db_session.scalars(remaining_cart_items_ids_statement).all() == []
        assert set(db_session.scalars(product_ids_statement).all()) == set(product_ids)

    def test_cant_clear_other_user_cart(self, db_session: Session) -> None:
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

        self.repository.delete_all_cart_items(self.user.id)

        other_user_cart_items_statement = select(CartItem.id).where(
            CartItem.cart_id == cart_two.id
        )
        my_items_statement = select(CartItem.id).where(CartItem.cart_id == cart_one.id)

        assert db_session.scalars(my_items_statement).all() == []
        assert db_session.scalars(other_user_cart_items_statement).all() == [
            cart_item_two.id
        ]
