import hashlib

import pytest
from redis import Redis

from app.repositories.auth.session_repository import SessionRepository


class TestUserIdByAccess:
    @pytest.fixture(autouse=True)
    def setup_data(self, redis_client: Redis, session_repository: SessionRepository):
        self.redis_client = redis_client
        self.session_repository = session_repository

    def test_get_user_id_by_access(self) -> None:
        access_token = 'test-access-token'
        access_hash = hashlib.sha256(access_token.encode()).hexdigest()

        self.redis_client.set(
            name=f'shop:access:{access_hash}',
            value=1,
            ex=60,
        )

        assert self.session_repository.get_user_id_by_access(access_token) == 1

    def test_if_acces_doesnt_exist(self) -> None:
        assert (
            self.session_repository.get_user_id_by_access('access-not-valid-token')
            is None
        )
