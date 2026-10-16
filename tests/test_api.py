from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["demo_mode"] is True


def test_scenarios_endpoint():
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    payload = response.json()
    assert "scenarios" in payload
    assert len(payload["scenarios"]) >= 4


def test_valid_investigation_request():
    response = client.post(
        "/api/investigations/analyze",
        json={
            "transaction_id": "TXN-90377",
            "customer_id": "CUST-1042",
            "amount": 2450.00,
            "merchant": "Northwind Luxury Goods",
            "device_id": "DEV-NEW-781",
            "location": "Dubai, UAE",
            "channel": "web",
            "alert_type": "transaction",
            "notes": "Password reset preceded the order.",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["risk_score"] >= 0
    assert payload["risk_band"] in {"low", "medium", "high"}
    assert payload["human_review_required"] is True
    assert payload["disclaimer"]


def test_invalid_investigation_request():
    response = client.post(
        "/api/investigations/analyze",
        json={
            "transaction_id": "TX",
            "customer_id": "C",
            "amount": 0,
            "merchant": "",
            "device_id": "D",
            "location": "",
        },
    )
    assert response.status_code == 400


def test_retrieve_saved_investigation():
    response = client.post(
        "/api/investigations/analyze",
        json={
            "transaction_id": "TXN-88422",
            "customer_id": "CUST-2108",
            "amount": 182.40,
            "merchant": "Pine Street Coffee",
            "device_id": "DEV-033",
            "location": "Seattle, WA",
            "channel": "mobile",
            "alert_type": "transaction",
        },
    )
    investigation = response.json()
    get_response = client.get(f"/api/investigations/{investigation['investigation_id']}")
    assert get_response.status_code == 200
    assert get_response.json()["risk_band"] in {"low", "medium", "high"}
