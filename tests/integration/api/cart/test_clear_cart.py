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
class TestClearCart:
    def test_if_not_authorized(self) -> None:
        with TestClient(app) as client:
            response = client.delete('/api/v1/cart/items')

        assert response.status_code == 401


    @pytest.mark.usefixtures('authorized_user')
    def test_no_cart(self, user: User) -> None:

        with TestClient(app) as client:
            response = client.delete('/api/v1/cart/items')

            assert response.status_code == 200


    @pytest.mark.usefixtures('authorized_user')
    def test_empty_cart(self, user: User, db_session: Session) -> None:
        cart = Cart(user_id=user.id)
        db_session.add(cart)
        db_session.flush()


        with TestClient(app) as client:
            response = client.delete('/api/v1/cart/items')

            assert response.status_code == 200

        cart_statement = select(Cart.id).where(Cart.user_id == user.id)
        items_statement = select(CartItem.id).where(CartItem.cart_id == cart.id)

        assert db_session.execute(cart_statement).scalar_one() == cart.id
        assert db_session.scalars(items_statement).all() == []


    @pytest.mark.usefixtures('authorized_user')
    def test_clear_cart_with_items(self, user: User, db_session: Session) -> None:
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

        db_session.add_all([
            CartItem(cart_id=cart.id, product_id=product_one.id, count=2),
            CartItem(cart_id=cart.id, product_id=product_two.id, count=3),
        ])
        db_session.flush()


        with TestClient(app) as client:
            response = client.delete('/api/v1/cart/items')

            assert response.status_code == 200

        cart_statement = select(Cart.id).where(Cart.user_id == user.id)
        items_statement = select(CartItem.id).where(CartItem.cart_id == cart.id)
        product_ids = {product_one.id, product_two.id}
        products_statement = select(Product.id).where(Product.id.in_(product_ids))

        assert db_session.execute(cart_statement).scalar_one() == cart.id
        assert db_session.scalars(items_statement).all() == []
        assert set(db_session.scalars(products_statement).all()) == product_ids


    @pytest.mark.usefixtures('authorized_user')
    def test_cant_clear_other_user_cart(self, user: User, db_session: Session) -> None:
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


        with TestClient(app) as client:
            response = client.delete('/api/v1/cart/items')

            assert response.status_code == 200

        my_items_statement = select(CartItem.id).where(CartItem.cart_id == my_cart.id)
        other_items_statement = select(CartItem.id).where(CartItem.cart_id == other_cart.id)

        assert db_session.scalars(my_items_statement).all() == []
        assert db_session.scalars(other_items_statement).all() == [other_item.id]
