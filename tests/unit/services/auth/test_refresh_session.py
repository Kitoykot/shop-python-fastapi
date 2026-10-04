from unittest.mock import Mock

import pytest

from app.dto.auth.token_info_dto import TokenInfoDto
from app.dto.user.user_dto import UserDto
from app.exceptions.auth.unauthorized_exception import UnauthorizedException
from app.exceptions.auth.user_is_not_active_exception import UserIsNotActiveException
from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.services.auth.password_service import PasswordService


class TestRefreshSession:
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
        self.session_repository.get_user_id_by_refresh.return_value = None

        with pytest.raises(UnauthorizedException):
            self.service.refresh_session('refresh-token')

        self.session_repository.get_user_id_by_refresh.assert_called_once_with('refresh-token')

        self.user_repository.find_user_by_id.assert_not_called()
        self.session_repository.refresh_session.assert_not_called()

    def test_if_user_is_none(self) -> None:
        self.session_repository.get_user_id_by_refresh.return_value = 1
        self.user_repository.find_user_by_id.return_value = None

        with pytest.raises(UnauthorizedException):
            self.service.refresh_session('refresh-token')

        self.session_repository.get_user_id_by_refresh.assert_called_once_with('refresh-token')
        self.user_repository.find_user_by_id.assert_called_once_with(1)
        
        self.session_repository.refresh_session.assert_not_called()

    def test_if_user_is_not_active(self) -> None:
        self.session_repository.get_user_id_by_refresh.return_value = 1
        self.user_repository.find_user_by_id.return_value = UserDto(
            id=1,
            password_hash='password-hash',
            is_active=False,
        )

        with pytest.raises(UserIsNotActiveException):
            self.service.refresh_session('refresh-token')

        self.session_repository.get_user_id_by_refresh.assert_called_once_with('refresh-token')
        self.user_repository.find_user_by_id.assert_called_once_with(1)
        
        self.session_repository.refresh_session.assert_not_called()


    def test_if_tokens_is_none(self) -> None:
        self.session_repository.get_user_id_by_refresh.return_value = 1
        self.user_repository.find_user_by_id.return_value = UserDto(
            id=1,
            password_hash='password-hash',
            is_active=True,
        )
        self.session_repository.refresh_session.return_value = None

        with pytest.raises(UnauthorizedException):
            self.service.refresh_session('refresh-token')

        self.session_repository.get_user_id_by_refresh.assert_called_once_with('refresh-token')
        self.user_repository.find_user_by_id.assert_called_once_with(1)
        self.session_repository.refresh_session.assert_called_once_with(
            refresh_token='refresh-token',
            expected_user_id=1,
        )


    def test_refresh_session(self) -> None:
        self.session_repository.get_user_id_by_refresh.return_value = 1
        self.user_repository.find_user_by_id.return_value = UserDto(
            id=1,
            password_hash='password-hash',
            is_active=True,
        )
        self.session_repository.refresh_session.return_value = TokenInfoDto(
            access_token='new-acces-token',
            refresh_token='new-refresh-token',
            access_token_expires_at='2026-10-22 11:00:00',
            refresh_token_expires_at='2026-10-29 11:00:00',
        )

        result = self.service.refresh_session('refresh-token')

        self.session_repository.get_user_id_by_refresh.assert_called_once_with('refresh-token')
        self.user_repository.find_user_by_id.assert_called_once_with(1)
        self.session_repository.refresh_session.assert_called_once_with(
            refresh_token='refresh-token',
            expected_user_id=1,
        )

        assert result is not None
        assert result.access_token == 'new-acces-token'
        assert result.refresh_token == 'new-refresh-token'
        assert result.access_token_expires_at == '2026-10-22 11:00:00'
        assert result.refresh_token_expires_at == '2026-10-29 11:00:00'