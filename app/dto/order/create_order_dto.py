from dataclasses import dataclass


@dataclass
class CreateOrderDto:
    user_name: str
    user_phone_number: str
    user_email: str | None
    user_city: str
    user_address: str
