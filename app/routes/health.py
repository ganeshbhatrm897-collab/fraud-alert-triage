from fastapi import APIRouter

from app.config import APP_NAME, APP_VERSION, settings

router = APIRouter(prefix="/api")


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
        "demo_mode": settings.demo_mode,
        "llm_configured": bool(settings.llm_enabled and settings.llm_api_key),
    }
