import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///nabilai_local.db")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "dev-secret-change-me"
    PROJECT_NAME: str = "NabilAI"
    GOOGLE_DRIVE_CREDENTIALS_JSON: str = ""

settings = Settings()
