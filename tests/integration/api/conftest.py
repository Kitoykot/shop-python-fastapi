from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from app.dependencies.auth.current_user_dependency import get_current_user
from app.dependencies.db.db_dependency import get_db
from app.dto.user.user_dto import UserDto
from app.main import app
from app.models.user.user import User


@pytest.fixture
def override_db(db_session: Session) -> Generator[None, None, None]:
    previous_overrides = app.dependency_overrides.copy()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield
    finally:
        app.dependency_overrides = previous_overrides


@pytest.fixture
def authorized_user(override_db: None, user: User) -> Generator[UserDto, None, None]:
    previous_overrides = app.dependency_overrides.copy()
    current_user = UserDto(
        id=user.id,
        password_hash=user.password_hash,
        is_active=user.is_active,
    )

    def override_get_current_user() -> UserDto:
        return current_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        yield current_user
    finally:
        app.dependency_overrides = previous_overrides
