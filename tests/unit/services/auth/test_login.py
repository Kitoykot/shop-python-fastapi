from unittest.mock import Mock

import pytest

from app.dto.auth.login.user_login_dto import UserLoginDto
from app.dto.auth.tokens.token_info_dto import TokenInfoDto
from app.dto.user.read.data.user_data_dto import UserDataDto
from app.exceptions.auth.user_is_not_active_exception import UserIsNotActiveException
from app.exceptions.auth.wrong_email_or_password_exception import (
    WrongEmailOrPasswordException,
)
from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.services.auth.password_service import PasswordService


class TestLogin:
    def setup_method(self):
        self.user_repository = Mock(spec=UserRepository)
        self.session_repository = Mock(spec=SessionRepository)
        self.password_service = Mock(spec=PasswordService)

        self.service = AuthService(
            user_repository=self.user_repository,
            session_repository=self.session_repository,
            password_service=self.password_service,
        )

    def test_if_user_is_none(self) -> None:
        self.user_repository.find_user_by_email.return_value = None

        with pytest.raises(WrongEmailOrPasswordException):
            self.service.login(
                UserLoginDto(email='user@test.com', password='qwerty1234')
            )

        self.user_repository.find_user_by_email.assert_called_once_with('user@test.com')

        self.password_service.verify.assert_not_called()
        self.session_repository.create_token.assert_not_called()

    def test_if_user_password_is_not_verified(self) -> None:
        user_dto = UserDataDto(
            id=1,
            password_hash='password_hash',
            is_active=True,
        )

        self.user_repository.find_user_by_email.return_value = user_dto
        self.password_service.verify.return_value = False

        with pytest.raises(WrongEmailOrPasswordException):
            self.service.login(
                UserLoginDto(email='user@test.com', password='qwerty1234')
            )

        self.user_repository.find_user_by_email.assert_called_once_with('user@test.com')
        self.password_service.verify.assert_called_once_with(
            password='qwerty1234', password_hash='password_hash'
        )

        self.session_repository.create_token.assert_not_called()

    def test_if_user_is_not_active(self) -> None:
        user_dto = UserDataDto(
            id=1,
            password_hash='password_hash',
            is_active=False,
        )

        self.user_repository.find_user_by_email.return_value = user_dto
        self.password_service.verify.return_value = True

        with pytest.raises(UserIsNotActiveException):
            self.service.login(
                UserLoginDto(email='user@test.com', password='qwerty1234')
            )

        self.user_repository.find_user_by_email.assert_called_once_with('user@test.com')
        self.password_service.verify.assert_called_once_with(
            password='qwerty1234', password_hash='password_hash'
        )

        self.session_repository.create_token.assert_not_called()

    def test_successful_login(self) -> None:
        user_dto = UserDataDto(
            id=1,
            password_hash='password_hash',
            is_active=True,
        )

        self.user_repository.find_user_by_email.return_value = user_dto
        self.password_service.verify.return_value = True
        self.session_repository.create_token.return_value = TokenInfoDto(
            access_token='acces-token',
            refresh_token='refresh-token',
            access_token_expires_at='2026-10-22 11:00:00',
            refresh_token_expires_at='2026-10-29 11:00:00',
        )

        result = self.service.login(
            UserLoginDto(email='user@test.com', password='qwerty1234')
        )

        assert result.access_token == 'acces-token'
        assert result.refresh_token == 'refresh-token'
        assert result.access_token_expires_at == '2026-10-22 11:00:00'
        assert result.refresh_token_expires_at == '2026-10-29 11:00:00'

        self.user_repository.find_user_by_email.assert_called_once_with('user@test.com')
        self.password_service.verify.assert_called_once_with(
            password='qwerty1234', password_hash='password_hash'
        )
        self.session_repository.create_token.assert_called_once_with(1)
