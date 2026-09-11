import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "NabilAI"

    # ==========================================
    # OpenRouter
    # ==========================================

    OPENROUTER_API_KEY: str = os.getenv(
        "OPENROUTER_API_KEY",
        ""
    )

    OPENROUTER_TEXT_MODEL: str = os.getenv(
        "OPENROUTER_TEXT_MODEL",
        "openrouter/free"
    )

    OPENROUTER_VISION_MODEL: str = os.getenv(
        "OPENROUTER_VISION_MODEL",
        "openrouter/free"
    )

    # ==========================================
    # Gemini
    # ==========================================

    GEMINI_API_KEY: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    GEMINI_API_KEY_2: str = os.getenv(
        "GEMINI_API_KEY_2",
        ""
    )

    GEMINI_API_KEY_3: str = os.getenv(
        "GEMINI_API_KEY_3",
        ""
    )

    GEMINI_API_KEY_4: str = os.getenv(
        "GEMINI_API_KEY_4",
        ""
    )

    GEMINI_API_KEY_5: str = os.getenv(
        "GEMINI_API_KEY_5",
        ""
    )

    GEMINI_TEXT_MODEL: str = os.getenv(
        "GEMINI_TEXT_MODEL",
        "gemini-3.6-flash"
    )

    GEMINI_VISION_MODEL: str = os.getenv(
        "GEMINI_VISION_MODEL",
        "gemini-3.6-flash"
    )

    # ==========================================
    # Groq
    # ==========================================

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_TEXT_MODEL: str = os.getenv(
        "GROQ_TEXT_MODEL",
        "openai/gpt-oss-120b"
    )

    # ==========================================
    # OpenAI - Fallback
    # ==========================================

    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    OPENAI_TEXT_MODEL: str = os.getenv(
        "OPENAI_TEXT_MODEL",
        "gpt-5.5"
    )

    OPENAI_VISION_MODEL: str = os.getenv(
        "OPENAI_VISION_MODEL",
        "gpt-5.5"
    )

    # ==========================================
    # Subscription / Trial
    # ==========================================

    NABIL_TRIAL_DAYS: int = int(
        os.getenv(
            "NABIL_TRIAL_DAYS",
            "30"
        )
    )

    NABIL_MONTHLY_PRICE_USD: float = float(
        os.getenv(
            "NABIL_MONTHLY_PRICE_USD",
            "5"
        )
    )

    WHISH_RECEIVER_NUMBER: str = os.getenv(
        "WHISH_RECEIVER_NUMBER",
        ""
    )

    # ==========================================
    # Security
    # ==========================================

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        ""
    )

    # ==========================================
    # Google Drive
    # ==========================================

    GOOGLE_DRIVE_CREDENTIALS_JSON: str = os.getenv(
        "GOOGLE_DRIVE_CREDENTIALS_JSON",
        ""
    )

    # ==========================================
    # Database
    # ==========================================

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./nabil_school.db"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
