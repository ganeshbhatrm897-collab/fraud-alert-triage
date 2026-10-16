from __future__ import annotations

import os
from typing import Any

from app.config import settings


def llm_available() -> bool:
    return bool(settings.llm_enabled and settings.llm_api_key)


def optional_llm_summary(prompt: str) -> str | None:
    if not llm_available():
        return None

    try:
        if os.getenv("LLM_PROVIDER", "mock").lower() == "mock":
            return "LLM summary unavailable; safe demo mode is active."
        return f"Optional LLM summary: {prompt[:200]}"
    except Exception:
        return None
