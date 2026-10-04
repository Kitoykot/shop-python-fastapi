from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.cart.cart import Cart
from app.models.cart.cart_item import CartItem
from app.models.product.product import Product
from app.models.user.user import User


@pytest.mark.usefixtures('override_db')
class TestGetCartApi:
    def test_if_not_authorized(self) -> None:
        with TestClient(app) as client:
            response = client.get('/api/v1/cart')

            assert response.status_code == 401

    @pytest.mark.usefixtures('authorized_user')
    def test_empty_cart(self, user: User) -> None:

        with TestClient(app) as client:
            response = client.get('/api/v1/cart')

        assert response.status_code == 200
        assert response.json() == {
            'cart': {
                'items_count': 0,
                'total_price': 0.0,
            },
            'items': [],
        }

    @pytest.mark.usefixtures('authorized_user')
    def test_cart_with_available_items(self, user: User, db_session: Session) -> None:
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

        with TestClient(app) as client:
            response = client.get('/api/v1/cart')

            assert response.status_code == 200
            assert response.json() == {
                'cart': {
                    'items_count': 4,
                    'total_price': 62.0,
                },
                'items': [
                    {
                        'id': cart_item_one.id,
                        'product_id': product_one.id,
                        'name': 'Product 1',
                        'count': 2,
                        'price': 20.50,
                        'is_available': True,
                    },
                    {
                        'id': cart_item_two.id,
                        'product_id': product_two.id,
                        'name': 'Product 2',
                        'count': 2,
                        'price': 10.50,
                        'is_available': True,
                    },
                ],
            }

    @pytest.mark.usefixtures('authorized_user')
    def test_cart_if_one_item_is_not_available(
        self, user: User, db_session: Session
    ) -> None:
        cart = Cart(user_id=user.id)

        product_one = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=False,
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

        with TestClient(app) as client:
            response = client.get('/api/v1/cart')

            assert response.status_code == 200
            assert response.json() == {
                'cart': {
                    'items_count': 2,
                    'total_price': 21.0,
                },
                'items': [
                    {
                        'id': cart_item_one.id,
                        'product_id': product_one.id,
                        'name': 'Product 1',
                        'count': 2,
                        'price': 20.50,
                        'is_available': False,
                    },
                    {
                        'id': cart_item_two.id,
                        'product_id': product_two.id,
                        'name': 'Product 2',
                        'count': 2,
                        'price': 10.50,
                        'is_available': True,
                    },
                ],
            }
