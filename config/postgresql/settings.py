from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

database = Database()
