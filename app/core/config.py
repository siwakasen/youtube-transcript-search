# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    YOUTUBE_API_KEY: str = ""
    ENV: str = "DEV"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
