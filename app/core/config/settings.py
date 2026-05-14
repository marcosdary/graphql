from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo
from typing import Optional

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
    ALGORITHM: str

    zone_info: Optional[ZoneInfo] = ZoneInfo("America/Sao_Paulo") 


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

