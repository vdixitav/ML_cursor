ml_cursor

## Project Phases & Tracking

### Phase 0: System Foundations (Safety & Contracts)
Status: ⬜ Not Started
- Define ML workflow states
- Define allowed ML actions
- Define trust & artifact model

Improvement Scope:
- Add org-level policy overrides
- Add multi-tenant RBAC
### Phase 1: Core ML Agents (Baseline Capability)
Status: ⬜ Not Started
- Dataset profiling agent
- EDA agent
- Preprocessing pipeline agent
- Baseline model training agent
- Evaluation agent

Improvement Scope:
- Add advanced feature engineering
- Add time-series aware logic

### Phase 2: Trust & Validation Layer
Status: ⬜ Not Started
- Artifact schema validation
- Leakage detection
- Metric sanity checks
- Model card generation

Improvement Scope:
- Automated risk scoring
- Model comparison dashboards

### Phase 3: Explainability & Audit
Status: ⬜ Not Started
- Feature importance / SHAP
- Decision trace logs
- Audit trail per run

Improvement Scope:
- Fairness metrics
- Bias detection

### Phase 4: Orchestration & Automation
Status: ⬜ Not Started
- Supervisor agent
- Resume-from-failure logic
- Experiment tracking

Improvement Scope:
- DAG-based execution
- Parallel evaluation

### Phase 5: Production Readiness
Status: ⬜ Not Started
- Config-driven execution
- CI checks
- Model versioning
- Deployment template

Improvement Scope:
- Kubernetes jobs
- Canary releases

## Why This Design

This system prioritizes **trust over speed**.

Unlike general AI code generators, this platform:
- Restricts AI actions via policy
- Enforces ML best practices
- Produces inspectable outputs
- Prevents silent failures

The goal is not to replace ML engineers, but to:
- Reduce repetitive work
- Enforce correctness
- Improve production readiness




🧠 Why this structure is TRUSTABLE & PROD-LIKE
1️⃣ agents/

Har ML step ka alag agent

Single responsibility

Easy to test + audit

2️⃣ core/

Rules of the system

Agent kuch bhi nahi karega jo policy allow na kare

State machine ensures correct ML order

3️⃣ tools/

Pure helper functions

No decision making (agents decide, tools execute)

4️⃣ outputs/

Trust layer

Jo bhi model banega → tangible artifact milega

Kisi bhi step ko independently verify kar sakte ho

⚙️ VS Code Ready Config
.vscode/settings.json
{
  "python.defaultInterpreterPath": "venv/bin/python",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.typeCheckingMode": "basic"
}

.vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run ML Agent",
      "type": "python",
      "request": "launch",
      "program": "app/main.py",
      "console": "integratedTerminal"
    }
  ]
}

🏃 How you’ll work in VS Code (day-to-day)

1️⃣ Dataset data/ me dalo
2️⃣ app/main.py run karo
3️⃣ Agents sequentially run honge
4️⃣ outputs/ me artifacts generate honge
5️⃣ Tum har artifact open karke trust kar sakti ho

🧪 Example Run Flow
INGEST
  ↓
PROFILE  → data_profile.json
  ↓
EDA      → eda_report.md
  ↓
PREPROCESS → pipeline.pkl
  ↓
TRAIN     → model.pkl
  ↓
EVALUATE  → metrics.json
  ↓
EXPLAIN   → model_card.md

🔐 Production Safety Built-in

No arbitrary code execution

No file deletion

No external calls

ML-only allowlist

Deterministic metrics


## Task Specification

The system does not infer ML tasks implicitly.
Each run requires an explicit task configuration that defines:
- task type (regression / classification / forecasting)
- target column
- feature inclusion/exclusion
- evaluation metrics
- allowed models

This ensures correctness, auditability, and safe reuse of datasets
across multiple ML objectives.
