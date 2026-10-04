from collections.abc import Generator

import pytest
from redis import Redis
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.enums.user.user_role import UserRole
from app.models.user.user import User

TEST_DATABASE_URL = 'postgresql+psycopg://shop_test:shop_test@127.0.0.1:5433/shop_test'


@pytest.fixture(scope='session')
def db_engine() -> Generator[Engine, None, None]:
    engine = create_engine(TEST_DATABASE_URL)

    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    with db_engine.connect() as connection:
        transaction = connection.begin()

        try:
            with Session(
                bind=connection,
                autoflush=False,
                join_transaction_mode='create_savepoint',
            ) as session:
                yield session
        finally:
            transaction.rollback()


@pytest.fixture
def redis_client() -> Generator[Redis, None, None]:
    client = Redis(
        host='127.0.0.1',
        port=6380,
        db=0,
        decode_responses=True,
    )

    try:
        client.ping()
        client.flushdb()

        yield client
    finally:
        try:
            client.flushdb()
        finally:
            client.close()


@pytest.fixture
def user(db_session: Session) -> User:
    user = User(
        first_name='User',
        middle_name='Userovich',
        last_name='Userov',
        email='user@test.com',
        password_hash='test-hash',
        phone_number='78901234567',
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add(user)
    db_session.flush()

    return user
