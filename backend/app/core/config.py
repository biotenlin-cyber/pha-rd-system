from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://pha:pha@localhost:5432/pha"
    sync_database_url: str = "postgresql+psycopg://pha:pha@localhost:5432/pha"
    cors_origins: str = "http://localhost:5173"
    search_backend: str = "trgm"
    log_level: str = "INFO"

    anthropic_api_key: str = ""
    anthropic_default_model: str = "claude-sonnet-4-6"
    anthropic_oa_model: str = "claude-opus-4-7"
    anthropic_critique_model: str = "claude-haiku-4-5-20251001"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
