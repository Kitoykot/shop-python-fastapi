from dataclasses import dataclass


@dataclass
class UserDto:
    id: int
    password_hash: str
    is_active: bool
