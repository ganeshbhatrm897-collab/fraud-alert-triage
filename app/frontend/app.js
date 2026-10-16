const form = document.getElementById('investigation-form');
const scenarioButtonsContainer = document.getElementById('scenario-buttons');
const apiMessage = document.getElementById('api-message');
const loadingIndicator = document.getElementById('loading');
const riskScoreEl = document.getElementById('risk-score');
const riskBandEl = document.getElementById('risk-band');
const timelineEl = document.getElementById('timeline');
const supportingEvidenceEl = document.getElementById('supporting-evidence');
const contradictingEvidenceEl = document.getElementById('contradicting-evidence');
const missingInformationEl = document.getElementById('missing-information');
const recommendedNextStepEl = document.getElementById('recommended-next-step');
const humanReviewEl = document.getElementById('human-review');
const resetButton = document.getElementById('reset-button');

let scenarios = [];

function setMessage(text, type = '') {
  apiMessage.textContent = text;
  apiMessage.className = 'api-message';
  if (type) {
    apiMessage.classList.add(type);
  }
}

function renderScenarioButtons() {
  scenarioButtonsContainer.innerHTML = '';
  scenarios.forEach((scenario) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'scenario-btn';
    button.textContent = scenario.name;
    button.addEventListener('click', () => {
      document.querySelectorAll('.scenario-btn').forEach((btn) => btn.classList.remove('active'));
      button.classList.add('active');
      const defaults = scenario.defaults || {};
      Object.entries(defaults).forEach(([key, value]) => {
        const field = form.elements.namedItem(key);
        if (field) {
          field.value = value;
        }
      });
      setMessage(`Loaded scenario: ${scenario.name}`, 'success');
    });
    scenarioButtonsContainer.appendChild(button);
  });
}

function serializeForm() {
  const data = {};
  new FormData(form).forEach((value, key) => {
    data[key] = value;
  });
  data.amount = Number(data.amount || 0);
  if (!data.dispute_reason) {
    data.dispute_reason = null;
  }
  if (!data.notes) {
    data.notes = null;
  }
  return data;
}

function renderList(container, items) {
  container.innerHTML = '';
  if (!items || items.length === 0) {
    const empty = document.createElement('li');
    empty.textContent = 'No relevant items identified.';
    container.appendChild(empty);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    container.appendChild(li);
  });
}

function renderReport(report) {
  riskScoreEl.textContent = report.risk_score ?? '--';
  const band = report.risk_band || 'low';
  riskBandEl.textContent = `${band.toUpperCase()} RISK`;
  riskScoreEl.className = 'score-pill';
  riskBandEl.className = '';
  if (band === 'low') {
    riskScoreEl.classList.add('low-band');
    riskBandEl.classList.add('low-band');
  } else if (band === 'medium') {
    riskScoreEl.classList.add('medium-band');
    riskBandEl.classList.add('medium-band');
  } else {
    riskScoreEl.classList.add('high-band');
    riskBandEl.classList.add('high-band');
  }

  const findings = report.agent_findings || [];
  timelineEl.innerHTML = '';
  findings.forEach((agent) => {
    const li = document.createElement('li');
    li.textContent = `${agent.agent}: ${agent.summary}`;
    timelineEl.appendChild(li);
  });

  renderList(supportingEvidenceEl, report.supporting_evidence || []);
  renderList(contradictingEvidenceEl, report.contradicting_evidence || []);
  renderList(missingInformationEl, report.missing_information || []);

  recommendedNextStepEl.textContent = report.recommended_next_step || 'No recommendation yet.';
  humanReviewEl.textContent = report.human_review_required
    ? 'Human review required before consequential action.'
    : 'No immediate human review required for this advisory finding.';
}

async function loadScenarios() {
  const response = await fetch('/api/scenarios');
  const payload = await response.json();
  scenarios = payload.scenarios || [];
  renderScenarioButtons();
  if (scenarios.length > 0) {
    const first = scenarios[0];
    const firstDefaults = first.defaults || {};
    Object.entries(firstDefaults).forEach(([key, value]) => {
      const field = form.elements.namedItem(key);
      if (field) field.value = value;
    });
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  loadingIndicator.classList.remove('hidden');
  setMessage('Running investigation...', 'success');

  try {
    const response = await fetch('/api/investigations/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(serializeForm()),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || 'Investigation failed.');
    }
    renderReport(payload);
    setMessage('Investigation completed successfully.', 'success');
  } catch (error) {
    setMessage(error.message || 'Unexpected error while analyzing the alert.', 'error');
  } finally {
    loadingIndicator.classList.add('hidden');
  }
}

function resetForm() {
  form.reset();
  riskScoreEl.textContent = '--';
  riskBandEl.textContent = 'No report yet';
  riskBandEl.className = '';
  riskScoreEl.className = 'score-pill';
  timelineEl.innerHTML = '';
  supportingEvidenceEl.innerHTML = '';
  contradictingEvidenceEl.innerHTML = '';
  missingInformationEl.innerHTML = '';
  recommendedNextStepEl.textContent = 'No recommendation yet.';
  humanReviewEl.textContent = '';
  setMessage('Form reset.');
}

form.addEventListener('submit', handleSubmit);
resetButton.addEventListener('click', resetForm);
loadScenarios();
