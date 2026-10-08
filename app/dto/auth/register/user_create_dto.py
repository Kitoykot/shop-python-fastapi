from dataclasses import dataclass


@dataclass
class UserCreateDto:
    first_name: str
    middle_name: str | None
    last_name: str
    email: str
    password_hash: str
    phone_number: str
