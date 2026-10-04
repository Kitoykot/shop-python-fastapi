from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.user.user_role import UserRole
from app.main import app
from app.models.cart.cart import Cart
from app.models.cart.cart_item import CartItem
from app.models.product.product import Product
from app.models.user.user import User


@pytest.mark.usefixtures('override_db')
class TestDeleteItem:
    def test_if_not_authorized(self) -> None:
        with TestClient(app) as client:
            response = client.delete(url='/api/v1/cart/items/1')

            assert response.status_code == 401

    @pytest.mark.usefixtures('authorized_user')
    def test_not_valid_path_param(self, user: User) -> None:

        with TestClient(app) as client:
            response = client.delete(url='/api/v1/cart/items/abc')

            assert response.status_code == 422

    @pytest.mark.usefixtures('authorized_user')
    def test_detele_item(self, user: User, db_session: Session) -> None:
        cart = Cart(user_id=user.id)
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
            count=2,
        )
        cart_item_two = CartItem(
            cart_id=cart.id,
            product_id=product_two.id,
            count=2,
        )
        db_session.add_all([cart_item_one, cart_item_two])
        db_session.flush()

        cart_item_one_id = cart_item_one.id

        with TestClient(app) as client:
            response = client.delete(url=f'/api/v1/cart/items/{cart_item_one_id}')

            assert response.status_code == 200

        cart_statement = select(Cart).where(
            Cart.id == cart.id,
            Cart.user_id == user.id,
        )
        item_one_statement = select(CartItem).where(
            CartItem.id == cart_item_one_id,
            CartItem.cart_id == cart.id,
        )
        item_two_statement = select(CartItem).where(
            CartItem.id == cart_item_two.id,
            CartItem.cart_id == cart.id,
        )

        assert db_session.execute(cart_statement).scalar_one() is not None
        assert db_session.scalar(item_one_statement) is None
        assert db_session.execute(item_two_statement).scalar_one() is not None

    @pytest.mark.usefixtures('authorized_user')
    def test_cant_delete_other_user_item(self, user: User, db_session: Session) -> None:
        other_user = User(
            first_name='Other',
            middle_name=None,
            last_name='User',
            email='other-user@test.com',
            password_hash='test-hash',
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
        db_session.add_all([other_user, product])
        db_session.flush()

        my_cart = Cart(user_id=user.id)
        other_cart = Cart(user_id=other_user.id)
        db_session.add_all([my_cart, other_cart])
        db_session.flush()

        my_item = CartItem(cart_id=my_cart.id, product_id=product.id, count=2)
        other_item = CartItem(cart_id=other_cart.id, product_id=product.id, count=3)
        db_session.add_all([my_item, other_item])
        db_session.flush()

        cart_ids = [my_cart.id, other_cart.id]
        expected_item_ids = {my_item.id, other_item.id}

        with TestClient(app) as client:
            response = client.delete(url=f'/api/v1/cart/items/{other_item.id}')

            assert response.status_code == 200

        statement = select(CartItem.id).where(CartItem.cart_id.in_(cart_ids))
        remaining_item_ids = db_session.scalars(statement).all()

        assert set(remaining_item_ids) == expected_item_ids

    @pytest.mark.usefixtures('authorized_user')
    def test_delete_item_that_doesnt_exist(
        self, user: User, db_session: Session
    ) -> None:
        cart = Cart(user_id=user.id)
        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=20,
        )
        db_session.add_all([cart, product])
        db_session.flush()

        item = CartItem(cart_id=cart.id, product_id=product.id, count=2)
        db_session.add(item)
        db_session.flush()

        with TestClient(app) as client:
            response = client.delete(url=f'/api/v1/cart/items/{item.id}')
            assert response.status_code == 200

            item_statement = select(CartItem.id).where(CartItem.id == item.id)
            assert db_session.scalar(item_statement) is None

            response = client.delete(url=f'/api/v1/cart/items/{item.id}')
            assert response.status_code == 200

        cart_statement = select(Cart.id).where(Cart.user_id == user.id)
        assert db_session.execute(cart_statement).scalar_one() == cart.id

    @pytest.mark.usefixtures('authorized_user')
    def test_delete_item_without_cart(self, user: User) -> None:

        with TestClient(app) as client:
            response = client.delete(url='/api/v1/cart/items/1')

            assert response.status_code == 200
