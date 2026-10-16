from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.models import InvestigationRequest
from app.services.investigation_service import analyze_investigation, get_investigation_by_id

router = APIRouter(prefix="/api/investigations")


@router.get("/")
def list_placeholder() -> dict:
    return {"message": "Use /api/scenarios or POST /api/investigations/analyze."}


@router.get("/{investigation_id}")
def get_investigation(investigation_id: str) -> dict[str, Any]:
    investigation = get_investigation_by_id(investigation_id)
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    return investigation


@router.post("/analyze")
def analyze(request: InvestigationRequest) -> dict[str, Any]:
    try:
        return analyze_investigation(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
