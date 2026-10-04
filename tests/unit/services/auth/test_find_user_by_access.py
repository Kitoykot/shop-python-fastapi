from unittest.mock import Mock

import pytest

from app.dto.user.user_dto import UserDto
from app.exceptions.auth.unauthorized_exception import UnauthorizedException
from app.exceptions.auth.user_is_not_active_exception import UserIsNotActiveException
from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.services.auth.password_service import PasswordService


class TestFindUserByAccess:
    def setup_method(self):
        self.user_repository = Mock(spec=UserRepository)
        self.session_repository = Mock(spec=SessionRepository)
        self.password_service = Mock(spec=PasswordService)

        self.service = AuthService(
            user_repository=self.user_repository,
            session_repository=self.session_repository,
            password_service=self.password_service,
        )

    def test_if_user_id_is_none(self) -> None:
        self.session_repository.get_user_id_by_access.return_value = None

        with pytest.raises(UnauthorizedException):
            self.service.find_user_by_access_token('access-token')

        self.session_repository.get_user_id_by_access.assert_called_once_with(
            'access-token'
        )

        self.user_repository.find_user_by_id.assert_not_called()

    def test_if_user_is_none(self) -> None:
        self.session_repository.get_user_id_by_access.return_value = 1
        self.user_repository.find_user_by_id.return_value = None

        with pytest.raises(UnauthorizedException):
            self.service.find_user_by_access_token('access-token')

        self.session_repository.get_user_id_by_access.assert_called_once_with(
            'access-token'
        )
        self.user_repository.find_user_by_id.assert_called_once_with(1)

    def test_if_user_is_not_active(self) -> None:
        self.session_repository.get_user_id_by_access.return_value = 1
        self.user_repository.find_user_by_id.return_value = UserDto(
            id=1,
            password_hash='password-hash',
            is_active=False,
        )

        with pytest.raises(UserIsNotActiveException):
            self.service.find_user_by_access_token('access-token')

        self.session_repository.get_user_id_by_access.assert_called_once_with(
            'access-token'
        )
        self.user_repository.find_user_by_id.assert_called_once_with(1)

    def test_get_user_by_access(self) -> None:
        self.session_repository.get_user_id_by_access.return_value = 1
        self.user_repository.find_user_by_id.return_value = UserDto(
            id=1,
            password_hash='password-hash',
            is_active=True,
        )

        result = self.service.find_user_by_access_token('access-token')

        self.session_repository.get_user_id_by_access.assert_called_once_with(
            'access-token'
        )
        self.user_repository.find_user_by_id.assert_called_once_with(1)

        assert result is not None
        assert result.id == 1
        assert result.password_hash == 'password-hash'
        assert result.is_active is True
