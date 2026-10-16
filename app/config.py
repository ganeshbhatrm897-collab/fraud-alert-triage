import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "app" / "frontend"

APP_NAME = "Agentic Fraud Alert Triage & Dispute Resolution"
APP_VERSION = "0.1.0"


def get_env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    app_name = APP_NAME
    app_version = APP_VERSION
    demo_mode = True
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    llm_base_url = os.getenv("LLM_BASE_URL")
    llm_enabled = get_env_bool("LLM_ENABLED", False) and bool(llm_api_key)


settings = Settings()
