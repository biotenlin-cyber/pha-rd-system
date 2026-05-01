from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://pha:pha@localhost:5432/pha"
    sync_database_url: str = "postgresql+psycopg://pha:pha@localhost:5432/pha"
    cors_origins: str = "http://localhost:5173"
    search_backend: str = "trgm"
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
