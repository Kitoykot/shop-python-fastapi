from pydantic import BaseModel, EmailStr, Field

from app.dto.auth.user_login_dto import UserLoginDto


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=254)
    password: str = Field(min_length=8, max_length=256)

    def create_dto(self) -> UserLoginDto:
        return UserLoginDto(
            email=self.email,
            password=self.password,
        )