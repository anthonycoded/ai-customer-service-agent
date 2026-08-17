import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/ai_customer_service",
)
class Settings(BaseSettings):
    database_url: str = DATABASE_URL

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()