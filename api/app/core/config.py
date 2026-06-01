from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str = "postgresql+asyncpg://esport_user:esport_pass@localhost:5432/esport_db"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ISSUER: str = "sit-unizd-esport"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_scheme(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        if v and v.startswith("postgresql://") and not v.startswith("postgresql+asyncpg://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
