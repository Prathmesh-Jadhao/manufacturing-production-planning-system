from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5432/manufacturing_db"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:8501", "http://127.0.0.1:8501"]
    LOG_LEVEL: str = "INFO"
    WORKING_DAYS: int = 22
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()