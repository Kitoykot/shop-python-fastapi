from pydantic_settings import BaseSettings, SettingsConfigDict


class MailSettings(BaseSettings):
    smtp_host: str
    smtp_port: int
    smtp_from: str

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    )


mail_settings = MailSettings()
