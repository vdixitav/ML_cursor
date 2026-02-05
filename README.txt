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
