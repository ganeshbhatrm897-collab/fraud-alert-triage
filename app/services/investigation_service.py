from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

from app.agents.customer_history_agent import run_customer_history_analysis
from app.agents.device_location_agent import run_device_location_analysis
from app.agents.dispute_evidence_agent import run_dispute_evidence_analysis
from app.agents.intake_agent import run_intake
from app.agents.resolution_agent import run_resolution_agent
from app.agents.risk_assessment_agent import run_risk_assessment
from app.agents.transaction_agent import run_transaction_analysis
from app.models import InvestigationRequest
from app.services.demo_data import get_scenario
from app.services.llm_service import optional_llm_summary

INVESTIGATION_STORE: dict[str, dict] = {}


def _build_request(payload: dict) -> InvestigationRequest:
    scenario_name = payload.get("scenario")
    scenario = get_scenario(scenario_name)
    merged = deepcopy(scenario)
    for key, value in payload.items():
        if value is not None and value != "":
            merged[key] = value
    return InvestigationRequest.model_validate(merged)


def _summarize_transaction(request: InvestigationRequest, scenario: dict) -> dict:
    profile = scenario.get("customer_profile", {})
    return {
        "transaction_id": request.transaction_id,
        "customer_id": request.customer_id,
        "amount": round(float(request.amount), 2),
        "merchant": request.merchant,
        "device_id": request.device_id,
        "location": request.location,
        "channel": request.channel,
        "alert_type": request.alert_type,
        "customer_profile": {
            "average_monthly_spend": profile.get("average_monthly_spend", 0),
            "known_devices": profile.get("known_devices", []),
            "common_locations": profile.get("common_locations", []),
        },
    }


def analyze_investigation(payload: dict) -> dict:
    request = _build_request(payload)
    scenario_name = payload.get("scenario") or request.scenario or "suspicious_high_value"
    scenario = get_scenario(scenario_name)

    intake = run_intake(request)
    transaction = run_transaction_analysis(request, scenario)
    device_location = run_device_location_analysis(request, scenario)
    customer_history = run_customer_history_analysis(request, scenario)
    dispute_evidence = run_dispute_evidence_analysis(request, scenario)

    agent_findings = [
        intake,
        transaction,
        device_location,
        customer_history,
        dispute_evidence,
    ]

    risk_result = run_risk_assessment(agent_findings)
    resolution = run_resolution_agent(risk_result, payload)

    llm_hint = optional_llm_summary(
        f"Customer {request.customer_id} transaction {request.transaction_id} requires review in {scenario['name']}."
    )
    if llm_hint:
        risk_result["llm_note"] = llm_hint

    supporting_evidence = []
    contradicting_evidence = []
    missing_information = []

    for finding in agent_findings:
        supporting_evidence.extend(finding.get("evidence", []))
        missing_information.extend(finding.get("missing_information", []))

    for evidence in risk_result.get("contradicting_evidence", []):
        contradicting_evidence.append(evidence)

    for signal in risk_result.get("signals", []):
        supporting_evidence.append(signal)

    resolution_missing = resolution.get("missing_information", [])
    missing_information.extend(resolution_missing)
    deduped_missing = []
    seen = set()
    for item in missing_information:
        key = item.lower().strip()
        if key and key not in seen:
            deduped_missing.append(item)
            seen.add(key)

    investigation_id = str(uuid4())
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    report = {
        "investigation_id": investigation_id,
        "timestamp": timestamp,
        "scenario": scenario["name"],
        "transaction_summary": _summarize_transaction(request, scenario),
        "risk_score": int(risk_result["risk_score"]),
        "risk_band": risk_result["risk_band"],
        "agent_findings": [
            intake,
            transaction,
            device_location,
            customer_history,
            dispute_evidence,
            risk_result,
            resolution,
        ],
        "supporting_evidence": supporting_evidence,
        "contradicting_evidence": contradicting_evidence,
        "missing_information": deduped_missing,
        "recommended_next_step": resolution["next_step"],
        "rationale": resolution["rationale"],
        "human_review_required": bool(resolution["human_review_required"]),
        "disclaimer": "This is a simulated advisory report for educational use only. It is not a final fraud determination and requires human review for consequential action.",
    }
    INVESTIGATION_STORE[investigation_id] = report
    return report


def get_investigation_by_id(investigation_id: str) -> dict | None:
    return INVESTIGATION_STORE.get(investigation_id)
