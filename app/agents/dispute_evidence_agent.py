from __future__ import annotations

from app.models import InvestigationRequest


def run_dispute_evidence_analysis(request: InvestigationRequest, scenario: dict) -> dict:
    signals: list[str] = []
    missing: list[str] = []
    evidence: list[str] = []

    if request.alert_type == "dispute":
        if request.dispute_reason:
            signals.append(f"The customer dispute cites: {request.dispute_reason}.")
            evidence.append(f"Dispute reason: {request.dispute_reason}.")
        else:
            missing.append("Customer dispute reason")
        if request.notes:
            evidence.append(f"Customer notes: {request.notes}")
        else:
            missing.append("Customer narrative or supporting notes")

        if request.dispute_reason and "not received" in request.dispute_reason.lower():
            missing.append("Tracking number or courier confirmation")
            missing.append("Delivery timestamp or proof of receipt")
            evidence.append("The dispute is supported by the customer's narrative but lacks shipping proof.")
        else:
            evidence.append("There is preliminary dispute information but not enough to confirm or reject the claim.")
    else:
        signals.append("No formal dispute evidence is provided for this transaction alert.")
        evidence.append("Transaction review is active and dispute documentation remains optional.")

    return {
        "agent": "Dispute and Evidence Agent",
        "status": "ok",
        "summary": "Dispute evidence review identifies what is available and what remains missing.",
        "signals": signals,
        "missing_information": missing,
        "evidence": evidence,
    }
