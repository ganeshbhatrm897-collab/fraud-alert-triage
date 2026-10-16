# Agentic Fraud Alert Triage & Dispute Resolution

A simulated financial-fraud investigation dashboard and API that demonstrates transparent, agent-based triage for transaction alerts and dispute claims. The project uses deterministic demo logic by default and is designed to be safe: every recommendation is advisory and requires human review before any consequential financial action.

## Overview

This project is an educational, fictional workflow that accepts a transaction alert or dispute, analyzes it across several specialized investigation agents, and returns a structured risk report. It includes:

- A FastAPI backend with validation and investigation orchestration
- A lightweight, browser-based dashboard built with HTML, CSS, and vanilla JavaScript
- Four demo scenarios that model normal, suspicious, incomplete, and conflicting evidence states
- Deterministic risk scoring and human-review guidance
- Optional LLM integration configured through environment variables, but defaulting to safe demo behavior

## Features

- Simulated data only; no real customer or financial information
- Risk score from 0 to 100 with low/medium/high banding
- Separate agent modules for intake, transaction analysis, device/location checks, account history, dispute evidence, risk assessment, and resolution guidance
- API endpoints for health checks, scenario catalog, investigation analysis, and historical lookup
- Front-end dashboard for live demonstration and interactive scenario selection
- Pytest suite covering API flows, agent logic, validation, and safety checks

## Agent responsibilities

1. Intake and Triage Agent
   - Validates the alert, identifies the transaction or dispute type, and normalizes the incoming data.
2. Transaction Analysis Agent
   - Evaluates merchant, amount, and deviations from a synthetic customer profile.
3. Device and Location Agent
   - Reviews device familiarity and geographic mismatch signals.
4. Customer History Agent
   - Compares current activity to synthetic account history and common behavior.
5. Dispute and Evidence Agent
   - Summarizes the evidence set and highlights missing or conflicting information.
6. Risk Assessment Agent
   - Combines documented signals into a transparent risk score and risk band.
7. Resolution Recommendation Agent
   - Recommends the next action and clearly states whether human review is required.

## Workflow

The service orchestrates each agent sequentially and returns a single structured investigation report. Risk scores and recommendations are clearly stated so a user can see the basis for the decision without hidden chain-of-thought.

## Folder structure

```text
fraud-alert-triage/
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── intake_agent.py
│   │   ├── transaction_agent.py
│   │   ├── device_location_agent.py
│   │   ├── customer_history_agent.py
│   │   ├── dispute_evidence_agent.py
│   │   ├── risk_assessment_agent.py
│   │   └── resolution_agent.py
│   ├── frontend/
│   │   ├── app.js
│   │   ├── index.html
│   │   └── styles.css
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── investigations.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── demo_data.py
│   │   ├── investigation_service.py
│   │   └── llm_service.py
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── models.py
├── tests/
│   ├── test_agents.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── .venv/
```

## Python setup on Windows PowerShell

```powershell
cd C:\Users\HP\fraud-alert-triage
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the application

```powershell
cd C:\Users\HP\fraud-alert-triage
.\.venv\Scripts\Activate.ps1
python run.py
```

Then open the browser at:

- http://127.0.0.1:8000/

## API endpoints

### Health check

```bash
curl http://127.0.0.1:8000/api/health
```

### Available scenarios

```bash
curl http://127.0.0.1:8000/api/scenarios
```

### Analyze a transaction or dispute

```bash
curl -X POST http://127.0.0.1:8000/api/investigations/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-90377",
    "customer_id": "CUST-1042",
    "amount": 2450,
    "merchant": "Northwind Luxury Goods",
    "device_id": "DEV-NEW-781",
    "location": "Dubai, UAE",
    "channel": "web",
    "alert_type": "transaction",
    "notes": "Customer reported the order immediately after a password reset."
  }'
```

### Retrieve a prior investigation

```bash
curl http://127.0.0.1:8000/api/investigations/{investigation_id}
```

## Demo scenarios

The app ships with four synthetic scenarios:

- Suspicious high-value transaction
- Normal customer pattern
- Dispute with incomplete evidence
- Conflicting signals requiring human review

All records are clearly labeled as simulated and are designed to demonstrate how evidence can be gathered without turning a risk signal into a final fraud decision.

## Testing

```powershell
cd C:\Users\HP\fraud-alert-triage
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

The suite checks:

- Health and scenario endpoints
- Valid and invalid investigation requests
- Agent behavior for key signals
- Risk-score bounds and band consistency
- Demo-mode safety and graceful handling of missing configuration
- Retrieval of previously generated investigations

## Optional LLM configuration

Set environment variables like this in a local `.env` file:

```env
LLM_API_KEY=your-api-key
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.example.com/v1
LLM_ENABLED=true
```

If the environment is not configured or the provider call fails, the application falls back to deterministic demo logic and never exposes secrets. LLM output, if present, is treated as advisory and cannot bypass the human review requirement.

## Security limits and human review safeguards

This is an educational simulation, not a real banking workflow. The tool is intentionally designed so it cannot autonomously:

- freeze or reopen accounts
- reverse transactions
- reject disputes
- transfer funds
- make irreversible financial determinations

Any recommendation that could have consequential action is marked as requiring human review. The application keeps secrets out of API responses and intentionally avoids hard-coded credentials.

## Example response

```json
{
  "investigation_id": "...",
  "timestamp": "2026-10-16T12:00:00Z",
  "scenario": "Suspicious high-value transaction",
  "risk_score": 64,
  "risk_band": "medium",
  "recommended_next_step": "Request additional evidence and monitor the activity while a human investigator checks the account context.",
  "human_review_required": true,
  "disclaimer": "This is a simulated advisory report for educational use only. It is not a final fraud determination and requires human review for consequential action."
}
```

## Known limitations

- The application uses synthetic data and deterministic rules rather than real fraud analytics.
- It does not integrate with a bank system or real payment rails.
- LLM support is optional and intentionally limited to a safe, non-critical advisory path.

## Suggested GitHub repository name

`fraud-alert-triage`

## License

This project is intended for educational and portfolio use in a simulated environment. Add an appropriate license if you intend to publish it publicly on GitHub.
