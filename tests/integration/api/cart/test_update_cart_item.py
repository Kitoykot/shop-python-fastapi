from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.main import app
from app.models.cart.cart import Cart
from app.models.cart.cart_item import CartItem
from app.models.product.product import Product
from app.models.user.user import User


@pytest.mark.usefixtures('override_db')
class TestUpdateCartItem:
    def test_if_not_authorized(self) -> None:
        with TestClient(app) as client:
            response = client.post(
                url='/api/v1/cart/items',
                json={
                    'product_id': 15,
                    'count': 2,
                },
            )

            assert response.status_code == 401

    @pytest.mark.usefixtures('authorized_user')
    def test_if_no_payload(self, user: User) -> None:

        with TestClient(app) as client:
            response = client.post(url='/api/v1/cart/items')

            assert response.status_code == 422

    @pytest.mark.parametrize(
        ('payload', 'missing_field'),
        [
            ({'count': 2}, 'product_id'),
            ({'product_id': 1}, 'count'),
        ],
    )
    @pytest.mark.usefixtures('authorized_user')
    def test_required_field_is_missing(
        self,
        user: User,
        payload: dict,
        missing_field: str,
    ) -> None:

        with TestClient(app) as client:
            response = client.post(url='/api/v1/cart/items', json=payload)

            assert response.status_code == 422

            errors = response.json()['detail']

            assert errors[0]['type'] == 'missing'
            assert errors[0]['loc'] == ['body', missing_field]

    @pytest.mark.parametrize(
        ('payload', 'problem_field', 'type_error'),
        [
            ({'product_id': 1, 'count': 0}, 'count', 'greater_than'),
            ({'product_id': 1, 'count': -1}, 'count', 'greater_than'),
            ({'product_id': 1, 'count': 32768}, 'count', 'less_than_equal'),
            ({'product_id': 1, 'count': 'one'}, 'count', 'int_parsing'),
            ({'product_id': 1, 'count': None}, 'count', 'int_type'),
            ({'product_id': 0, 'count': 1}, 'product_id', 'greater_than'),
            ({'product_id': -1, 'count': 1}, 'product_id', 'greater_than'),
            ({'product_id': 'one', 'count': 1}, 'product_id', 'int_parsing'),
            ({'product_id': None, 'count': 1}, 'product_id', 'int_type'),
        ],
    )
    @pytest.mark.usefixtures('authorized_user')
    def test_payload_field_is_invalid(
        self,
        user: User,
        payload: dict,
        problem_field: str,
        type_error: str,
    ) -> None:

        with TestClient(app) as client:
            response = client.post(url='/api/v1/cart/items', json=payload)

            assert response.status_code == 422

            errors = response.json()['detail']

            assert errors[0]['type'] == type_error
            assert errors[0]['loc'] == ['body', problem_field]

    @pytest.mark.usefixtures('authorized_user')
    def test_if_product_not_found(self, user: User, db_session: Session) -> None:
        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=False,
            count=20,
        )

        db_session.add(product)
        db_session.flush()

        product_id = product.id

        db_session.delete(product)
        db_session.flush()

        with TestClient(app) as client:
            response = client.post(
                url='/api/v1/cart/items',
                json={
                    'product_id': product_id,
                    'count': 2,
                },
            )

            assert response.status_code == 404

    @pytest.mark.usefixtures('authorized_user')
    def test_if_product_not_showed_in_catalog(
        self, user: User, db_session: Session
    ) -> None:
        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=False,
            count=20,
        )

        db_session.add(product)
        db_session.flush()

        with TestClient(app) as client:
            response = client.post(
                url='/api/v1/cart/items',
                json={
                    'product_id': product.id,
                    'count': 2,
                },
            )

            assert response.status_code == 404

    @pytest.mark.usefixtures('authorized_user')
    def test_if_products_count_is_zero(self, user: User, db_session: Session) -> None:
        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=0,
        )

        db_session.add(product)
        db_session.flush()

        with TestClient(app) as client:
            response = client.post(
                url='/api/v1/cart/items',
                json={
                    'product_id': product.id,
                    'count': 2,
                },
            )

            assert response.status_code == 404

    @pytest.mark.usefixtures('authorized_user')
    def test_create_cart_item(self, user: User, db_session: Session) -> None:
        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=10,
        )

        db_session.add(product)
        db_session.flush()

        with TestClient(app) as client:
            response = client.post(
                url='/api/v1/cart/items',
                json={
                    'product_id': product.id,
                    'count': 2,
                },
            )

            assert response.status_code == 200

        cart_statement = select(Cart).where(Cart.user_id == user.id)
        cart = db_session.execute(cart_statement).scalar_one()

        item_statement = select(CartItem).where(CartItem.cart_id == cart.id)
        item = db_session.execute(item_statement).scalar_one()

        assert item is not None
        assert item.product_id == product.id
        assert item.count == 2

    @pytest.mark.usefixtures('authorized_user')
    def test_update_cart_item(self, user: User, db_session: Session) -> None:
        cart = Cart(user_id=user.id)
        product = Product(
            name='Product 1',
            description='Product 1 description',
            price=Decimal('20.50'),
            show_in_catalog=True,
            count=10,
        )

        db_session.add_all([cart, product])
        db_session.flush()

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            count=12,
        )

        db_session.add(cart_item)
        db_session.flush()

        with TestClient(app) as client:
            response = client.post(
                url='/api/v1/cart/items',
                json={
                    'product_id': product.id,
                    'count': 2,
                },
            )

            assert response.status_code == 200

        cart_statement = select(Cart).where(Cart.user_id == user.id)
        cart = db_session.execute(cart_statement).scalar_one()

        item_statement = select(CartItem).where(CartItem.cart_id == cart.id)
        item = db_session.execute(item_statement).scalar_one()

        assert item is not None
        assert item.id == cart_item.id
        assert item.product_id == product.id
        assert item.count == 2
