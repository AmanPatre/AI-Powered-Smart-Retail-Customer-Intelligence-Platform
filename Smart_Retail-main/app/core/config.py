"""Application configuration module using Pydantic Settings."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings configuration for Smart Retail Platform."""

    PROJECT_NAME: str = "Smart Retail & Customer Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = ""
    DEBUG: bool = True

    # Security
    API_KEY: str = "smart_retail_secret_key_2026"
    API_KEY_NAME: str = "X-API-Key"

    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models_saved"
    UPLOADS_DIR: Path = BASE_DIR / "data" / "uploads"

    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/smart_retail.db"

    # ML Model Configs
    INTENTS_FILE: Path = BASE_DIR / "data" / "intents.json"
    SENTIMENT_MODEL_PATH: Path = BASE_DIR / "models_saved" / "sentiment_pipeline.pkl"
    PRODUCT_MODEL_PATH: Path = BASE_DIR / "models_saved" / "mobilenet_retail.h5"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

# Ensure required data/model directories exist on startup
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
