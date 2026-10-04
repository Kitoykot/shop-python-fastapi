import hashlib

import pytest
from redis import Redis

from app.repositories.auth.session_repository import SessionRepository


class TestClearSession:
    @pytest.fixture(autouse=True)
    def setup_data(self, redis_client: Redis, session_repository: SessionRepository):
        self.redis_client = redis_client
        self.session_repository = session_repository


    def test_if_no_session(self) -> None:
        assert self.session_repository.clear_session('refresh-token') is None

    def test_clear_session(self) -> None:
        access_token = 'access-token'
        refresh_token = 'refresh-token'

        access_hash = hashlib.sha256(access_token.encode()).hexdigest()
        refresh_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

        access_key = f'shop:access:{access_hash}'
        refresh_key = f'shop:refresh:{refresh_hash}'

        self.redis_client.set(
            name=access_key,
            value=1,
            ex=60,
        )
        self.redis_client.hset(
            name=refresh_key,
            mapping={
                'user_id': 1,
                'access_hash': access_hash,
            }
        )
        self.redis_client.expire(name=refresh_key, time=60)

        self.session_repository.clear_session(refresh_token)

        assert self.redis_client.exists(access_key) == 0
        assert self.redis_client.exists(refresh_key) == 0


    def test_clear_session_if_two_sessions(self) -> None:
        access_token_one = 'access-token-one'
        refresh_token_one = 'refresh-token-one'

        access_hash_one = hashlib.sha256(access_token_one.encode()).hexdigest()
        refresh_hash_one = hashlib.sha256(refresh_token_one.encode()).hexdigest()

        access_key_one = f'shop:access:{access_hash_one}'
        refresh_key_one = f'shop:refresh:{refresh_hash_one}'

        access_token_two = 'access-token-two'
        refresh_token_two = 'refresh-token-two'

        access_hash_two = hashlib.sha256(access_token_two.encode()).hexdigest()
        refresh_hash_two = hashlib.sha256(refresh_token_two.encode()).hexdigest()

        access_key_two = f'shop:access:{access_hash_two}'
        refresh_key_two = f'shop:refresh:{refresh_hash_two}'

        self.redis_client.set(
            name=access_key_one,
            value=1,
            ex=60,
        )
        self.redis_client.hset(
            name=refresh_key_one,
            mapping={
                'user_id': 1,
                'access_hash': access_hash_one,
            }
        )
        self.redis_client.expire(name=refresh_key_one, time=60)

        self.redis_client.set(
            name=access_key_two,
            value=1,
            ex=60,
        )
        self.redis_client.hset(
            name=refresh_key_two,
            mapping={
                'user_id': 1,
                'access_hash': access_hash_two,
            }
        )
        self.redis_client.expire(name=refresh_key_two, time=60)

        self.session_repository.clear_session(refresh_token_one)

        assert self.redis_client.exists(access_key_one) == 0
        assert self.redis_client.exists(refresh_key_one) == 0

        assert self.redis_client.exists(access_key_two) == 1
        assert self.redis_client.exists(refresh_key_two) == 1