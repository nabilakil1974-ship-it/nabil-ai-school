import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "NabilAI"

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    OPENAI_TEXT_MODEL: str = "gpt-5.6"
    OPENAI_VISION_MODEL: str = "gpt-5.6"

    OPENAI_TRANSCRIPTION_MODEL: str = "gpt-4o-transcribe"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    GOOGLE_DRIVE_CREDENTIALS_JSON: str = os.getenv(
        "GOOGLE_DRIVE_CREDENTIALS_JSON",
        ""
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./nabil_school.db"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
