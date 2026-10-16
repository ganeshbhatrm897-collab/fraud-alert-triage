from __future__ import annotations

from app.models import InvestigationRequest


def run_intake(request: InvestigationRequest) -> dict:
    alert_type = request.alert_type
    summary = (
        f"Intake accepted a {alert_type} alert for customer {request.customer_id} and transaction {request.transaction_id}."
    )
    signals: list[str] = []
    missing: list[str] = []

    if not request.transaction_id:
        missing.append("transaction identifier")
    if not request.customer_id:
        missing.append("customer identifier")
    if request.alert_type == "dispute" and not request.dispute_reason:
        missing.append("dispute reason")

    if request.alert_type == "transaction":
        signals.append("The alert is defined as a transaction review.")
    elif request.alert_type == "dispute":
        signals.append("The alert is defined as a customer dispute review.")

    evidence = [
        f"Channel: {request.channel}",
        f"Merchant: {request.merchant}",
        f"Device: {request.device_id}",
        f"Location: {request.location}",
    ]

    return {
        "agent": "Intake and Triage Agent",
        "status": "ok",
        "summary": summary,
        "signals": signals,
        "missing_information": missing,
        "evidence": evidence,
    }
