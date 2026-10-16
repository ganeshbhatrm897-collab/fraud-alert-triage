from app.agents.intake_agent import run_intake
from app.agents.risk_assessment_agent import run_risk_assessment
from app.agents.resolution_agent import run_resolution_agent
from app.models import InvestigationRequest
from app.services.demo_data import get_scenario


def test_intake_agent_handles_dispute():
    request = InvestigationRequest(
        transaction_id="TXN-101",
        customer_id="CUST-1",
        amount=199.00,
        merchant="Widget Shop",
        device_id="DEV-7",
        location="Austin, TX",
        alert_type="dispute",
        dispute_reason="Item not received",
        notes="Package never arrived.",
    )
    result = run_intake(request)
    assert result["agent"] == "Intake and Triage Agent"
    assert result["status"] == "ok"


def test_risk_assessment_score_is_bounded():
    findings = [
        {"signals": ["The device is unfamiliar to the customer profile.", "The location differs from the customer's recent activity."]},
        {"signals": ["Customer history is consistent with prior known device and location usage."]},
    ]
    result = run_risk_assessment(findings)
    assert 0 <= result["risk_score"] <= 100
    assert result["risk_band"] in {"low", "medium", "high"}


def test_resolution_requires_human_review_for_high_risk():
    risk_result = {"risk_band": "high"}
    resolution = run_resolution_agent(risk_result, {"alert_type": "transaction"})
    assert resolution["human_review_required"] is True


def test_scenario_baseline_is_normal_for_known_pattern():
    request = InvestigationRequest(
        transaction_id="TXN-88422",
        customer_id="CUST-2108",
        amount=182.40,
        merchant="Pine Street Coffee",
        device_id="DEV-033",
        location="Seattle, WA",
        channel="mobile",
        alert_type="transaction",
    )
    scenario = get_scenario("normal_customer_pattern")
    from app.agents.device_location_agent import run_device_location_analysis

    result = run_device_location_analysis(request, scenario)
    assert any("familiar" in signal.lower() for signal in result["signals"])
