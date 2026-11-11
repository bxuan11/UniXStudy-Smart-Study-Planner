from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    supabase_url: str = ""
    supabase_anon_key: SecretStr = SecretStr("")
    cors_origins: list[str] = []

@lru_cache
def get_settings() -> Settings:
    return Settings()
