from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class InvestigationRequest(BaseModel):
    transaction_id: str = Field(..., min_length=3, max_length=64)
    customer_id: str = Field(..., min_length=3, max_length=64)
    amount: float = Field(..., gt=0)
    merchant: str = Field(..., min_length=2, max_length=128)
    device_id: str = Field(..., min_length=3, max_length=64)
    location: str = Field(..., min_length=2, max_length=128)
    channel: str = Field(default="mobile", min_length=2, max_length=32)
    alert_type: Literal["transaction", "dispute"] = "transaction"
    scenario: str | None = None
    dispute_reason: str | None = None
    notes: str | None = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be greater than zero.")
        return value


class AgentFinding(BaseModel):
    agent: str
    status: str
    summary: str
    signals: list[str] = []
    missing_information: list[str] = []
    evidence: list[str] = []


class InvestigationReport(BaseModel):
    investigation_id: str
    timestamp: str
    scenario: str
    transaction_summary: dict[str, Any]
    risk_score: int
    risk_band: Literal["low", "medium", "high"]
    agent_findings: list[dict[str, Any]]
    supporting_evidence: list[str]
    contradicting_evidence: list[str]
    missing_information: list[str]
    recommended_next_step: str
    rationale: str
    human_review_required: bool
    disclaimer: str
