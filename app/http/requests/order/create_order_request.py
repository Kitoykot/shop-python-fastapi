from pydantic import BaseModel, EmailStr, Field, field_validator

from app.dto.order.create_order_dto import CreateOrderDto


class CreateOrderRequest(BaseModel):
    user_name: str = Field(min_length=5, max_length=128)
    user_phone_number: str = Field(min_length=4, max_length=16, pattern=r'^[0-9]+$')
    user_email: EmailStr | None = Field(max_length=254, default=None)
    user_city: str = Field(min_length=3, max_length=255)
    user_address: str = Field(min_length=5, max_length=500)

    @field_validator('user_phone_number', mode='before')
    @classmethod
    def normalize_phone_number(cls, value: object) -> object:
        if isinstance(value, str):
            return value.translate(str.maketrans('', '', '+()- '))

        return value

    def create_dto(self) -> CreateOrderDto:
        return CreateOrderDto(
            user_name=self.user_name,
            user_phone_number=self.user_phone_number,
            user_email=self.user_email,
            user_city=self.user_city,
            user_address=self.user_address,
        )
