from pwdlib import PasswordHash


class PasswordService:
    def __init__(self):
        self.hasher = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.hasher.hash(password=password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self.hasher.verify(password=password, hash=password_hash)
