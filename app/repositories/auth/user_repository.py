from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.dto.auth.register.user_create_dto import UserCreateDto
from app.dto.user.read.data.user_data_dto import UserDataDto
from app.enums.user.user_role import UserRole
from app.models.user.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def exists_by_email(self, email: str) -> bool:
        statement = select(exists(User).where(User.email == email))

        return bool(self.session.scalar(statement))

    def exists_by_phone_number(self, phone_number: str) -> bool:
        statement = select(exists(User).where(User.phone_number == phone_number))

        return bool(self.session.scalar(statement))

    def create_user(self, dto: UserCreateDto) -> None:
        user = User(
            first_name=dto.first_name,
            middle_name=dto.middle_name,
            last_name=dto.last_name,
            email=dto.email,
            password_hash=dto.password_hash,
            phone_number=dto.phone_number,
            is_active=True,
            role=UserRole.USER,
        )

        self.session.add(user)
        self.session.commit()

    def find_user_by_email(self, email: str) -> UserDataDto | None:
        statement = select(User).where(User.email == email)
        user = self.session.scalar(statement)

        if user is None:
            return None

        return self.__to_dto(user)

    def find_user_by_id(self, user_id: int) -> UserDataDto | None:
        statement = select(User).where(User.id == user_id)
        user = self.session.scalar(statement)

        if user is None:
            return None

        return self.__to_dto(user)

    def __to_dto(self, user: User) -> UserDataDto:
        return UserDataDto(
            id=user.id, password_hash=user.password_hash, is_active=user.is_active
        )
