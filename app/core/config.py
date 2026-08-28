import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    مُحيطاً، أو الـ .env ) إعدادات المشروع - تقرأ تلقائياً من متغيرات البيئة
    (مباشرة عند النشر من Railway من إعدادات).
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///nabilai_local.db")
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "dev-secret-change-me"
    PROJECT_NAME: str = "NabilAI"
    GOOGLE_DRIVE_CREDENTIALS_JSON: str = ""

settings = Settings()
