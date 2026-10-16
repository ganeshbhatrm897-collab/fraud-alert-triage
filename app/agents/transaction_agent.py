from __future__ import annotations

from app.models import InvestigationRequest


def run_transaction_analysis(request: InvestigationRequest, scenario: dict) -> dict:
    signals: list[str] = []
    missing: list[str] = []
    evidence: list[str] = []
    score = 0

    customer_profile = scenario.get("customer_profile", {})
    avg_spend = float(customer_profile.get("average_monthly_spend", 0) or 0)
    amount = float(request.amount)

    if amount > avg_spend * 2.5:
        signals.append("The amount is substantially above the customer's normal spending pattern.")
        evidence.append(f"Amount ${amount:,.2f} exceeds the typical spend benchmark of ${avg_spend:,.2f}.")
        score += 25
    else:
        signals.append("The amount is reasonably aligned with the customer's normal spend range.")
        evidence.append("The amount is near the customer's established spend range.")

    if scenario.get("signals", {}).get("merchant_irregularity"):
        signals.append("The merchant is outside the customer's usual purchase pattern.")
        evidence.append(f"Merchant {request.merchant} is not typical for this customer profile.")
        score += 20

    if scenario.get("signals", {}).get("amount_deviation"):
        signals.append("The transaction amount is unusually high relative to the customer's typical activity.")
        score += 15

    if request.merchant.lower() in {"northwind luxury goods", "jetstream travel"}:
        evidence.append("Merchant category is unusual for a routine customer purchase.")

    if not request.notes:
        missing.append("Customer-notes context for the purchase")

    return {
        "agent": "Transaction Analysis Agent",
        "status": "ok",
        "summary": (
            f"{request.merchant} transaction analysis indicates a {'higher-risk' if score >= 25 else 'consistent'} spend pattern."
        ),
        "signals": signals,
        "missing_information": missing,
        "evidence": evidence,
        "score": score,
    }
