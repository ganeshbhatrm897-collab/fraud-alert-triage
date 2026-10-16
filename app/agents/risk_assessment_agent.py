from __future__ import annotations


def run_risk_assessment(agent_findings: list[dict]) -> dict:
    score = 20
    supporting: list[str] = []
    contradicting: list[str] = []

    for finding in agent_findings:
        for signal in finding.get("signals", []):
            lower = signal.lower()
            if "unfamiliar" in lower or "substantially above" in lower or "not typical" in lower or "outside" in lower:
                score += 12
                supporting.append(signal)
            elif "consistent" in lower or "recognized" in lower or "matches" in lower:
                score -= 8
                contradicting.append(signal)

    if any("recent account activity" in signal.lower() for finding in agent_findings for signal in finding.get("signals", [])):
        score += 8
        supporting.append("Recent account activity suggests the login context changed.")

    if any("stable recent pattern" in signal.lower() for finding in agent_findings for signal in finding.get("signals", [])):
        score -= 10
        contradicting.append("Stable recent pattern reduces suspicion.")

    score = max(0, min(100, score))
    if score >= 70:
        band = "high"
    elif score >= 40:
        band = "medium"
    else:
        band = "low"

    return {
        "agent": "Risk Assessment Agent",
        "status": "ok",
        "summary": f"Evidence supports a {band} risk assessment with a score of {score} out of 100.",
        "risk_score": score,
        "risk_band": band,
        "signals": supporting,
        "contradicting_evidence": contradicting,
        "evidence": supporting,
    }
