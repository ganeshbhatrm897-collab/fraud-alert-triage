from __future__ import annotations

from app.models import InvestigationRequest


def run_device_location_analysis(request: InvestigationRequest, scenario: dict) -> dict:
    signals: list[str] = []
    missing: list[str] = []
    evidence: list[str] = []
    score = 0

    profile = scenario.get("customer_profile", {})
    known_devices = profile.get("known_devices", [])
    common_locations = profile.get("common_locations", [])

    if request.device_id in known_devices:
        signals.append("The device matches a familiar customer device.")
        evidence.append(f"Device {request.device_id} is recognized in the customer's profile.")
    else:
        signals.append("The device is unfamiliar to the customer profile.")
        evidence.append(f"Device {request.device_id} is not among the customer's known devices.")
        score += 25

    if request.location in common_locations:
        signals.append("The transaction originated from a commonly used customer location.")
        evidence.append(f"Location {request.location} matches known customer travel or residence.")
    else:
        signals.append("The location differs from the customer's recent and common activity.")
        evidence.append(f"Location {request.location} is outside previously seen customer locations.")
        score += 25

    if scenario.get("signals", {}).get("recent_password_reset"):
        signals.append("Recent account activity suggests a credential change may have preceded the transaction.")
        evidence.append("A recent password reset may have contributed to a new login pattern.")
        score += 10

    return {
        "agent": "Device and Location Agent",
        "status": "ok",
        "summary": (
            "Device and location review indicates a "
            f"{'higher risk' if score >= 20 else 'normal'} access pattern."
        ),
        "signals": signals,
        "missing_information": missing,
        "evidence": evidence,
        "score": score,
    }
