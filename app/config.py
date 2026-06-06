from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Microservice Resilience Platform"
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    METRICS_PORT: int = 8000
    REDIS_URL: str = "redis://localhost:6379/0"

    DATABASE_URL: str
    CICD_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ci_cd_database"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
