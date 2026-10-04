from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.dependencies.db.db_dependency import get_db
from app.dependencies.redis.redis_dependency import get_redis
from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.services.auth.password_service import PasswordService


def get_auth_service(
    db_session: Session = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
) -> AuthService:
    return AuthService(
        user_repository=UserRepository(db_session),
        session_repository=SessionRepository(redis_client),
        password_service=PasswordService(),
    )
