from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    إعدادات المشروع - تُقرأ تلقائياً من متغيرات البيئة (.env محلياً، أو
    من إعدادات Railway مباشرة عند النشر).
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    OPENAI_API_KEY: str = ""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///nabilai_local.db")
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "dev-secret-change-me"
    PROJECT_NAME: str = "NabilAI"
    GOOGLE_DRIVE_CREDENTIALS_JSON: str = ""


settings = Settings()
