from __future__ import annotations

from app.models import InvestigationRequest


def run_customer_history_analysis(request: InvestigationRequest, scenario: dict) -> dict:
    signals: list[str] = []
    missing: list[str] = []
    evidence: list[str] = []
    score = 0

    profile = scenario.get("customer_profile", {})
    known_devices = profile.get("known_devices", [])
    common_locations = profile.get("common_locations", [])
    avg_spend = profile.get("average_monthly_spend", 0)

    if request.device_id in known_devices and request.location in common_locations:
        signals.append("Customer history is consistent with prior known device and location usage.")
        evidence.append("The account has a stable recent pattern of device and location usage.")
    else:
        signals.append("Historical account behavior does not fully match the current transaction pattern.")
        evidence.append("Past account behavior does not neatly align with the current access and location signals.")
        score += 15

    if avg_spend and request.amount > avg_spend * 3:
        signals.append("The transaction is materially larger than the customer's typical monthly booking pattern.")
        evidence.append(f"The amount is over 3x the typical spend benchmark of ${avg_spend:,.2f}.")
        score += 15

    if request.alert_type == "dispute":
        signals.append("The customer dispute history should be reviewed for duplicate claims or recent service complaints.")
        evidence.append("Dispute context is relevant, but additional claim metadata is required for a full review.")
        score += 5

    return {
        "agent": "Customer History Agent",
        "status": "ok",
        "summary": "Customer history review highlights whether behavior aligns with prior account usage.",
        "signals": signals,
        "missing_information": missing,
        "evidence": evidence,
        "score": score,
    }
