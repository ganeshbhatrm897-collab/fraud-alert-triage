from __future__ import annotations


def run_resolution_agent(risk_result: dict, request: dict) -> dict:
    band = risk_result.get("risk_band", "low")
    if band == "high":
        next_step = "Escalate to a human investigator for immediate review and request account verification evidence."
        rationale = "High-risk indicators such as unfamiliar device usage, merchant irregularity, and location mismatch warrant human review before taking any consequential action."
        human_review_required = True
    elif band == "medium":
        next_step = "Request additional evidence and monitor the activity while a human investigator checks the account context."
        rationale = "The transaction shows mixed signals that are not definitive fraud, but they require a careful review and missing information should be collected."
        human_review_required = True
    else:
        next_step = "Continue monitoring and keep the transaction under standard review without additional blocking action."
        rationale = "The observed behavior is largely consistent with the customer's pattern and does not show a strong fraud signal on this evidence set."
        human_review_required = False

    missing = []
    if request.get("alert_type") == "dispute" and request.get("dispute_reason"):
        missing.extend([
            "Tracking or shipment evidence",
            "Proof of delivery or payment confirmation",
        ])
    elif band in {"medium", "high"}:
        missing.extend([
            "Additional login or device history",
            "Recent account security events",
        ])

    return {
        "agent": "Resolution Recommendation Agent",
        "status": "ok",
        "summary": next_step,
        "next_step": next_step,
        "rationale": rationale,
        "human_review_required": human_review_required,
        "missing_information": missing,
    }
