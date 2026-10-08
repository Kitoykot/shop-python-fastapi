from app.dto.auth.login.user_login_dto import UserLoginDto
from app.dto.auth.register.user_create_dto import UserCreateDto
from app.dto.auth.register.user_register_dto import UserRegisterDto
from app.dto.auth.tokens.token_info_dto import TokenInfoDto
from app.dto.user.read.data.user_data_dto import UserDataDto
from app.exceptions.auth.email_is_already_exists_exception import EmailIsAlreadyExists
from app.exceptions.auth.phone_is_already_exists_exception import (
    PhoneNumberIsAlreadyExists,
)
from app.exceptions.auth.unauthorized_exception import UnauthorizedException
from app.exceptions.auth.user_is_not_active_exception import UserIsNotActiveException
from app.exceptions.auth.wrong_email_or_password_exception import (
    WrongEmailOrPasswordException,
)
from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_repository import UserRepository
from app.services.auth.password_service import PasswordService


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
        password_service: PasswordService,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.password_service = password_service

    def register(self, dto: UserRegisterDto) -> None:
        if self.user_repository.exists_by_email(dto.email) is True:
            raise EmailIsAlreadyExists()

        if self.user_repository.exists_by_phone_number(dto.phone_number) is True:
            raise PhoneNumberIsAlreadyExists()

        user_create_dto = UserCreateDto(
            first_name=dto.first_name,
            middle_name=dto.middle_name,
            last_name=dto.last_name,
            email=dto.email,
            password_hash=self.password_service.hash(dto.password),
            phone_number=dto.phone_number,
        )

        self.user_repository.create_user(user_create_dto)

    def login(self, dto: UserLoginDto) -> TokenInfoDto:
        user = self.user_repository.find_user_by_email(dto.email)

        if user is None:
            raise WrongEmailOrPasswordException()

        if (
            self.password_service.verify(
                password=dto.password, password_hash=user.password_hash
            )
            is False
        ):
            raise WrongEmailOrPasswordException()

        if user.is_active is False:
            raise UserIsNotActiveException()

        return self.session_repository.create_token(user.id)

    def find_user_by_access_token(self, access_token: str) -> UserDataDto:
        user_id = self.session_repository.get_user_id_by_access(access_token)

        return self.__find_and_check_user_by_user_id(user_id)

    def refresh_session(self, refresh_token: str) -> TokenInfoDto:
        user_id = self.session_repository.get_user_id_by_refresh(refresh_token)
        self.__find_and_check_user_by_user_id(user_id)

        tokens = self.session_repository.refresh_session(
            refresh_token=refresh_token, expected_user_id=user_id
        )

        if tokens is None:
            raise UnauthorizedException()

        return tokens

    def logout(self, refresh_token: str) -> None:
        self.session_repository.clear_session(refresh_token)

    def __find_and_check_user_by_user_id(self, user_id: int | None) -> UserDataDto:
        if user_id is None:
            raise UnauthorizedException()

        user = self.user_repository.find_user_by_id(user_id)

        if user is None:
            raise UnauthorizedException()

        if user.is_active is False:
            raise UserIsNotActiveException()

        return user
