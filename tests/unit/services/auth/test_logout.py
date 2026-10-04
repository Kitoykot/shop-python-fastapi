from unittest.mock import Mock

from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.services.auth.password_service import PasswordService


class TestLogout:
    def setup_method(self):
        self.user_repository = Mock(spec=UserRepository)
        self.session_repository = Mock(spec=SessionRepository)
        self.password_service = Mock(spec=PasswordService)

        self.service = AuthService(
            user_repository=self.user_repository,
            session_repository=self.session_repository,
            password_service=self.password_service,
        )


    def test_logout(self) -> None:
        self.service.logout('refresh-token')

        self.session_repository.clear_session.assert_called_once_with('refresh-token')