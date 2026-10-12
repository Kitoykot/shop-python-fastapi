from dataclasses import dataclass

from app.enums.user.user_role import UserRole


@dataclass
class UserDataDto:
    id: int
    password_hash: str
    is_active: bool
    role: UserRole
