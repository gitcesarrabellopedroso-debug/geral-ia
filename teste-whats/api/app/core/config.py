from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Teste Whats API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    mongodb_uri: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URI")
    mongodb_db_name: str = Field(default="teste_whats", alias="MONGODB_DB_NAME")
    whatsapp_bridge_enabled: bool = Field(default=False, alias="WHATSAPP_BRIDGE_ENABLED")
    whatsapp_bridge_base_url: str = Field(default="http://localhost:8081", alias="WHATSAPP_BRIDGE_BASE_URL")
    whatsapp_bridge_timeout_seconds: float = Field(default=15.0, alias="WHATSAPP_BRIDGE_TIMEOUT_SECONDS")
    whatsapp_bridge_api_key: str = Field(default="", alias="WHATSAPP_BRIDGE_API_KEY")
    whatsapp_default_session_key: str = Field(default="principal", alias="WHATSAPP_DEFAULT_SESSION_KEY")
    backend_cors_origins: str = Field(default="*", alias="BACKEND_CORS_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        raw = self.backend_cors_origins.strip()
        if raw == "*":
            return ["*"]
        return [origin.strip() for origin in raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
