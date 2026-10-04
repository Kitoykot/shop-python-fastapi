from datetime import UTC, datetime, timedelta
import hashlib
import secrets

import pytest
from redis import Redis

from app.repositories.auth.session_repository import SessionRepository

from app.repositories.auth.session_repository import(
    ACCESS_TOKEN_EXPIRES_IN_SECONDS,
    REFRESH_TOKEN_EXPIRES_IN_SECONDS,
)

class TestUserIdByRefresh:
    @pytest.fixture(autouse=True)
    def setup_data(self, redis_client: Redis, session_repository: SessionRepository):
        self.redis_client = redis_client
        self.session_repository = session_repository


    def test_get_user_id_by_refresh(self) -> None:
        refresh_token = 'test-refresh-token'
        refresh_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        refresh_key = f'shop:refresh:{refresh_hash}'

        self.redis_client.hset(
            name=refresh_key,
            mapping={
                'user_id': 1,
                'access_hash': 'access-token-hash-test'
            },
        )
        self.redis_client.expire(refresh_key, 60)
        
        assert self.session_repository.get_user_id_by_refresh(refresh_token) == 1


    def test_if_refresh_doesnt_exist(self) -> None:
        assert self.session_repository.get_user_id_by_refresh('refresh-not-valid-token') is None