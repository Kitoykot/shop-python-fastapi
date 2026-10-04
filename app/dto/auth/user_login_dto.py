from dataclasses import dataclass


@dataclass
class UserLoginDto:
    email: str
    password: str