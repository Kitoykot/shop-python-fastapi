from dataclasses import dataclass


@dataclass
class TokenInfoDto:
    access_token: str
    refresh_token: str
    access_token_expires_at: str
    refresh_token_expires_at: str
