from dataclasses import dataclass


@dataclass
class UserDataDto:
    id: int
    password_hash: str
    is_active: bool
