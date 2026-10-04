import pytest
from redis import Redis

from app.repositories.auth.session_repository import SessionRepository


@pytest.fixture
def session_repository(redis_client: Redis) -> SessionRepository:
    return SessionRepository(redis_client)
