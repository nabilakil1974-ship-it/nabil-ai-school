import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "منصة الأستاذ نبيل - المنهاج اللبناني"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_DRIVE_CREDENTIALS_JSON: str = os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nabil_school.db")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
