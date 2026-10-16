from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, APP_VERSION, settings
from app.routes.health import router as health_router
from app.routes.investigations import router as investigations_router
from app.services.demo_data import SCENARIOS

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title=APP_NAME, version=APP_VERSION)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


app.include_router(health_router)
app.include_router(investigations_router)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/api/scenarios")
def scenario_list() -> dict:
    return {
        "service": APP_NAME,
        "demo_mode": settings.demo_mode,
        "scenarios": [
            {
                "id": key,
                "name": scenario["name"],
                "description": scenario["description"],
                "alert_type": scenario.get("alert_type", "transaction"),
                "defaults": scenario.get("defaults", {
                    "transaction_id": scenario.get("transaction_id"),
                    "customer_id": scenario.get("customer_id"),
                    "amount": scenario.get("amount"),
                    "merchant": scenario.get("merchant"),
                    "device_id": scenario.get("device_id"),
                    "location": scenario.get("location"),
                    "channel": scenario.get("channel"),
                    "alert_type": scenario.get("alert_type", "transaction"),
                    "notes": scenario.get("notes"),
                    "dispute_reason": scenario.get("dispute_reason", ""),
                }),
            }
            for key, scenario in SCENARIOS.items()
        ],
    }


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
