from pydantic import BaseModel, EmailStr, Field, field_validator

from app.dto.auth.user_register_dto import UserRegisterDto


class UserRegisterRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=64)
    middle_name: str | None = Field(default=None, min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=128)
    email: EmailStr = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8, max_length=256)
    phone_number: str = Field(
        min_length=4,
        max_length=16,
        pattern=r'^[0-9]+$',
    )

    @field_validator('phone_number', mode='before')
    @classmethod
    def normalize_phone_number(cls, value: object) -> object:
        if isinstance(value, str):
            return value.translate(str.maketrans('', '', '+()- '))

        return value

    def create_dto(self) -> UserRegisterDto:
        return UserRegisterDto(
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
            phone_number=self.phone_number,
        )
