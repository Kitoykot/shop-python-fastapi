from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )


redis_settings = RedisSettings()
