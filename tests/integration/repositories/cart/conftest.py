import pytest
from sqlalchemy.orm import Session

from app.repositories.cart.cart_repository import CartRepository


@pytest.fixture
def repository(db_session: Session) -> CartRepository:
    return CartRepository(db_session)
