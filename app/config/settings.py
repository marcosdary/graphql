from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    REDIS_URL: str
    DATABASE_URL: str
    DATABASE_URL_ASYNC: str

    CREATE_API_KEY: str
    PASSWORD_RESET_KEY: str
    TWO_FACTOR_AUTH_KEY: str
    SESSION_KEY: str

    API_KEY: str
    URL_NOTIFICATION_SYSTEM: str
    
    WEBHOOK_SECRET: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

