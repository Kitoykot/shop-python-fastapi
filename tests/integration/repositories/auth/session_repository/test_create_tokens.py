import hashlib

import pytest
from redis import Redis

from app.repositories.auth.session_repository import SessionRepository

from app.repositories.auth.session_repository import(
    ACCESS_TOKEN_EXPIRES_IN_SECONDS,
    REFRESH_TOKEN_EXPIRES_IN_SECONDS,
)


class TestCreateTokens:
    @pytest.fixture(autouse=True)
    def setup_data(self, redis_client: Redis, session_repository: SessionRepository):
        self.redis_client = redis_client
        self.session_repository = session_repository

    def test_create_tokens(self) -> None:
        tokens = self.session_repository.create_token(1)

        access_hash = hashlib.sha256(tokens.access_token.encode()).hexdigest()
        refresh_hash = hashlib.sha256(tokens.refresh_token.encode()).hexdigest()

        access_key = f'shop:access:{access_hash}'
        refresh_key = f'shop:refresh:{refresh_hash}'

        user_id_from_access = self.redis_client.get(access_key)
        data_by_refresh = self.redis_client.hgetall(refresh_key)

        access_ttl = self.redis_client.ttl(access_key)
        refresh_ttl = self.redis_client.ttl(refresh_key)

        assert user_id_from_access == '1'
        assert data_by_refresh['user_id'] == '1'
        assert data_by_refresh['access_hash'] == access_hash

        assert access_ttl > 0
        assert refresh_ttl > 0
        assert access_ttl <= ACCESS_TOKEN_EXPIRES_IN_SECONDS
        assert refresh_ttl <= REFRESH_TOKEN_EXPIRES_IN_SECONDS