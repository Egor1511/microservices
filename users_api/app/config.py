import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str
    TIMEOUT: int
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env"),
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
