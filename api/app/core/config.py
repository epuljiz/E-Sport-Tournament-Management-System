from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str = "postgresql+asyncpg://esport_user:esport_pass@localhost:5432/esport_db"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ISSUER: str = "sit-unizd-esport"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
