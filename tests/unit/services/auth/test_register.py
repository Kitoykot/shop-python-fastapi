from unittest.mock import Mock

import pytest

from app.dto.auth.register.user_create_dto import UserCreateDto
from app.dto.auth.register.user_register_dto import UserRegisterDto
from app.exceptions.auth.email_is_already_exists_exception import EmailIsAlreadyExists
from app.exceptions.auth.phone_is_already_exists_exception import (
    PhoneNumberIsAlreadyExists,
)
from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_repository import UserRepository
from app.services.auth.auth_service import AuthService
from app.services.auth.password_service import PasswordService


class TestRegister:
    def setup_method(self):
        self.user_repository = Mock(spec=UserRepository)
        self.session_repository = Mock(spec=SessionRepository)
        self.password_service = Mock(spec=PasswordService)

        self.service = AuthService(
            user_repository=self.user_repository,
            session_repository=self.session_repository,
            password_service=self.password_service,
        )

    def test_if_email_is_already_exist(self) -> None:
        self.user_repository.exists_by_email.return_value = True

        with pytest.raises(EmailIsAlreadyExists):
            self.service.register(
                UserRegisterDto(
                    first_name='User',
                    middle_name='Userovich',
                    last_name='Useriv',
                    email='email-test@gmail.com',
                    password='qwerty1234',
                    phone_number='89012345678',
                )
            )

        self.password_service.hash.assert_not_called()
        self.user_repository.create_user.assert_not_called()

    def test_if_phone_is_already_exist(self) -> None:
        self.user_repository.exists_by_email.return_value = False
        self.user_repository.exists_by_phone_number.return_value = True

        with pytest.raises(PhoneNumberIsAlreadyExists):
            self.service.register(
                UserRegisterDto(
                    first_name='User',
                    middle_name='Userovich',
                    last_name='Useriv',
                    email='email-test@gmail.com',
                    password='qwerty1234',
                    phone_number='89012345678',
                )
            )

        self.password_service.hash.assert_not_called()
        self.user_repository.create_user.assert_not_called()

    def test_successful_register(self) -> None:
        self.user_repository.exists_by_email.return_value = False
        self.user_repository.exists_by_phone_number.return_value = False
        self.password_service.hash.return_value = 'ajksjlsdkjfqwerty1234jdfhjksdfhkj'

        self.service.register(
            UserRegisterDto(
                first_name='User',
                middle_name='Userovich',
                last_name='Useriv',
                email='email-test@gmail.com',
                password='qwerty1234',
                phone_number='89012345678',
            )
        )

        self.password_service.hash.assert_called_once_with('qwerty1234')
        self.user_repository.create_user.assert_called_once_with(
            UserCreateDto(
                first_name='User',
                middle_name='Userovich',
                last_name='Useriv',
                email='email-test@gmail.com',
                password_hash='ajksjlsdkjfqwerty1234jdfhjksdfhkj',
                phone_number='89012345678',
            )
        )
