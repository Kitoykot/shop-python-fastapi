from dataclasses import dataclass


@dataclass
class UserRegisterDto:
    first_name: str
    middle_name: str | None
    last_name: str
    email: str
    password: str
    phone_number: str