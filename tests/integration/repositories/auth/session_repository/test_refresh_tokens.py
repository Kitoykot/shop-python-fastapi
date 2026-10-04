

import hashlib

import pytest
from redis import Redis

from app.repositories.auth.session_repository import(
    ACCESS_TOKEN_EXPIRES_IN_SECONDS,
    REFRESH_TOKEN_EXPIRES_IN_SECONDS,
    SessionRepository,
)


class TestRefreshTokens:
    @pytest.fixture(autouse=True)
    def setup_data(self, redis_client: Redis, session_repository: SessionRepository):
        self.redis_client = redis_client
        self.session_repository = session_repository


    def test_unknown_refresh_session(self) -> None:
        new_tokens = self.session_repository.refresh_session(
            refresh_token='old-refresh-token',
            expected_user_id=1
        )

        assert new_tokens is None


    def test_if_unexpected_user_id(self) -> None:
        old_access_token = 'old-access-token'
        old_refresh_token = 'old-refresh-token'

        old_access_hash = hashlib.sha256(old_access_token.encode()).hexdigest()
        old_refresh_hash = hashlib.sha256(old_refresh_token.encode()).hexdigest()

        old_access_key = f'shop:access:{old_access_hash}'
        old_refresh_key = f'shop:refresh:{old_refresh_hash}'

        self.redis_client.set(
            name=old_access_key,
            value=1,
            ex=60,
        )
        self.redis_client.hset(
            name=old_refresh_key,
            mapping={
                'user_id': 1,
                'access_hash': old_access_hash,
            }
        )
        self.redis_client.expire(name=old_refresh_key, time=60)

        new_tokens = self.session_repository.refresh_session(
            refresh_token=old_refresh_token,
            expected_user_id=2
        )

        assert new_tokens is None

        assert self.redis_client.get(old_access_key) == '1'
        assert self.redis_client.hgetall(old_refresh_key) == {
            'user_id': '1',
            'access_hash': old_access_hash,
        }

        

    def test_refresh_tokens(self) -> None:
        old_access_token = 'old-access-token'
        old_refresh_token = 'old-refresh-token'

        old_access_hash = hashlib.sha256(old_access_token.encode()).hexdigest()
        old_refresh_hash = hashlib.sha256(old_refresh_token.encode()).hexdigest()

        old_access_key = f'shop:access:{old_access_hash}'
        old_refresh_key = f'shop:refresh:{old_refresh_hash}'

        self.redis_client.set(
            name=old_access_key,
            value=1,
            ex=60,
        )
        self.redis_client.hset(
            name=old_refresh_key,
            mapping={
                'user_id': 1,
                'access_hash': old_access_hash,
            }
        )
        self.redis_client.expire(name=old_refresh_key, time=60)

        new_tokens = self.session_repository.refresh_session(
            refresh_token=old_refresh_token,
            expected_user_id=1
        )

        assert new_tokens is not None
        assert new_tokens.access_token != old_access_token
        assert new_tokens.refresh_token != old_refresh_token

        assert self.redis_client.exists(old_access_key) == 0
        assert self.redis_client.exists(old_refresh_key) == 0
        
        new_access_hash = hashlib.sha256(new_tokens.access_token.encode()).hexdigest()
        new_refresh_hash = hashlib.sha256(new_tokens.refresh_token.encode()).hexdigest()

        new_access_key = f'shop:access:{new_access_hash}'
        new_refresh_key = f'shop:refresh:{new_refresh_hash}'

        assert self.redis_client.get(new_access_key) == '1'
        assert self.redis_client.hgetall(new_refresh_key) == {
            'user_id': '1',
            'access_hash': new_access_hash,
        }

        access_ttl = self.redis_client.ttl(new_access_key)
        refresh_ttl = self.redis_client.ttl(new_refresh_key)

        assert access_ttl > 0
        assert refresh_ttl > 0

        assert access_ttl <= ACCESS_TOKEN_EXPIRES_IN_SECONDS
        assert refresh_ttl <= REFRESH_TOKEN_EXPIRES_IN_SECONDS