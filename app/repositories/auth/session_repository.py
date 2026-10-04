import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from redis import Redis
from redis.exceptions import WatchError

from app.dto.auth.token_info_dto import TokenInfoDto

ACCESS_TOKEN_EXPIRES_IN_SECONDS = 60 * 60 * 24 * 7
REFRESH_TOKEN_EXPIRES_IN_SECONDS = 60 * 60 * 24 * 7


class SessionRepository:
    def __init__(self, client: Redis):
        self.client = client

    def __get_token_hash(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def __token_key(self, token_type: str, token_hash: str) -> str:
        return f'shop:{token_type}:{token_hash}'

    def create_token(self, user_id: int) -> TokenInfoDto:
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)

        access_hash = self.__get_token_hash(access_token)
        refresh_hash = self.__get_token_hash(refresh_token)

        access_key = self.__token_key('access', access_hash)
        refresh_key = self.__token_key('refresh', refresh_hash)

        now = datetime.now(UTC).replace(microsecond=0)
        access_token_expires_at = now + timedelta(
            seconds=ACCESS_TOKEN_EXPIRES_IN_SECONDS
        )
        refresh_token_expires_at = now + timedelta(
            seconds=REFRESH_TOKEN_EXPIRES_IN_SECONDS
        )

        with self.client.pipeline(transaction=True) as pipeline:
            pipeline.set(
                name=access_key,
                value=user_id,
                exat=access_token_expires_at,
            )
            pipeline.hset(
                name=refresh_key,
                mapping={
                    'user_id': user_id,
                    'access_hash': access_hash,
                },
            )
            pipeline.expireat(name=refresh_key, when=refresh_token_expires_at)

            pipeline.execute()

        return TokenInfoDto(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_at=access_token_expires_at.isoformat(),
            refresh_token_expires_at=refresh_token_expires_at.isoformat(),
        )

    def get_user_id_by_refresh(self, refresh_token: str) -> int | None:
        refresh_key = self.__token_key(
            token_type='refresh', token_hash=self.__get_token_hash(refresh_token)
        )
        user_id = self.client.hget(refresh_key, 'user_id')

        if not user_id:
            return None

        return int(user_id)

    def get_user_id_by_access(self, access_token: str) -> int | None:
        access_key = self.__token_key(
            token_type='access', token_hash=self.__get_token_hash(access_token)
        )
        user_id = self.client.get(access_key)

        if not user_id:
            return None

        return int(user_id)

    def refresh_session(
        self,
        refresh_token: str,
        expected_user_id: int,
    ) -> TokenInfoDto | None:
        old_refresh_key = self.__token_key(
            token_type='refresh', token_hash=self.__get_token_hash(refresh_token)
        )

        with self.client.pipeline(transaction=True) as pipeline:
            try:
                pipeline.watch(old_refresh_key)

                old_session = pipeline.hgetall(old_refresh_key)

                if not old_session:
                    return None

                user_id = int(old_session.get('user_id'))

                if user_id != expected_user_id:
                    return None

                old_access_hash = old_session.get('access_hash')
                old_access_key = self.__token_key(
                    token_type='access', token_hash=old_access_hash
                )

                new_access_token = secrets.token_urlsafe(32)
                new_refresh_token = secrets.token_urlsafe(32)

                new_access_hash = self.__get_token_hash(new_access_token)
                new_refresh_hash = self.__get_token_hash(new_refresh_token)

                new_access_key = self.__token_key('access', new_access_hash)
                new_refresh_key = self.__token_key('refresh', new_refresh_hash)

                now = datetime.now(UTC).replace(microsecond=0)
                new_access_token_expires_at = now + timedelta(
                    seconds=ACCESS_TOKEN_EXPIRES_IN_SECONDS
                )
                new_refresh_token_expires_at = now + timedelta(
                    seconds=REFRESH_TOKEN_EXPIRES_IN_SECONDS
                )

                pipeline.multi()
                pipeline.delete(old_refresh_key, old_access_key)

                pipeline.set(
                    name=new_access_key,
                    value=user_id,
                    exat=new_access_token_expires_at,
                )
                pipeline.hset(
                    name=new_refresh_key,
                    mapping={
                        'user_id': user_id,
                        'access_hash': new_access_hash,
                    },
                )
                pipeline.expireat(
                    name=new_refresh_key, when=new_refresh_token_expires_at
                )

                pipeline.execute()
            except WatchError:
                return None

        return TokenInfoDto(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            access_token_expires_at=new_access_token_expires_at.isoformat(),
            refresh_token_expires_at=new_refresh_token_expires_at.isoformat(),
        )

    def clear_session(self, refresh_token: str) -> None:
        refresh_key = self.__token_key(
            token_type='refresh', token_hash=self.__get_token_hash(refresh_token)
        )
        refresh_session = self.client.hgetall(refresh_key)

        if not refresh_session:
            return None

        access_hash = refresh_session.get('access_hash')
        access_key = self.__token_key(token_type='access', token_hash=access_hash)

        self.client.delete(refresh_key, access_key)
