from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    app_name: str = "EduGenie"

    gemini_api_key: str = ""

    gemini_model: str = "gemini-3.8-flash"

    explanation_backend: str = "gemini"

    local_explanation_model: str = "MBZUAI/LLaMini-Flan-T5-783M"

    max_output_tokens: int = 1200

    temperature: float = 0.4

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()