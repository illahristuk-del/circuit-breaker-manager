import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


def read_secret_file(secret_name: str) -> Optional[str]:
    secret_path = f"/etc/secrets/{secret_name}"
    if os.path.exists(secret_path):
        with open(secret_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


class Settings(BaseSettings):
    PROJECT_NAME: str = "Microservice Resilience Platform"
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    METRICS_PORT: int = 8000
    REDIS_URL: str = "redis://localhost:6379/0"

    DATABASE_URL: Optional[str] = Field(default=None)
    CICD_DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ci_cd_database"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def __init__(self, **values):
        super().__init__(**values)
        val = read_secret_file("DATABASE_URL") or os.getenv("DATABASE_URL")
        if val:
            self.DATABASE_URL = val
        if not self.DATABASE_URL:
            raise ValueError("CRITICAL: DATABASE_URL is not configured!")


settings = Settings()
