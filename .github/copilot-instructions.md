# Copilot Repository Instructions — Taaqol Constitutional Repository

## Constitutional Priority

You are working in a constitutionally governed repository.

The root law is:

- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`

You must not treat instructions as suggestions. They are binding constraints.
Use `docs/20_AGENT_AUTONOMY_RUNBOOK.md` as the operational companion for
bounded next-safe-step selection.

## Current Constitutional State

- L0 is closed.
- L1 work is contract/audit bounded.
- L2 and L3 are locked.
- B0–B9 are internal L1 checkpoints only.
- Runtime remains embargoed.
- Euclidean Learning is `AUDIT_SANDBOX_ONLY`.
- Euclidean Learning outputs are non-authoritative.
- Domain boundary map is audit-only.
- FailureAlignment is audit-only.
- No runtime kernel is authorized.
- Computed coverage is schema/fixture based only.
- PR #103 added the `expected_verdict` fixture matrix; marker phrase: expected_verdict fixture matrix; do not regress it.
- computed_verdict cannot be supplied by fixture data.

## Forbidden Actions

Do not create or modify:

- `binding_kernel.py`
- `decision_engine.py`
- `coverage_matrix_v0.1.yaml`

Do not introduce:

- `Rank.CERTIFICATE`
- `Rank.REJECTED`
- `ExecutionRank.CERTIFIED` as runtime authority
- Boolean-as-proof fields:
  - `domain_proved: true`
  - `unit_proved: true`
  - `identity_preserved: true`
  - `trace_preserved: true`
  - `gate_passed: true`
  - `is_preserved: true`
- evidence list as proof
- identity preservation defaulting to true
- runtime predicates
- runtime translators
- manual `ComputedVerdict`
- runtime domain opening

Do not allow:

- `DAL_ONLY` to produce root, weight, word, tool, meaning, isnad, ifadah, hukm, or tanzil.
- `LAFZI_FORM` to produce lexical meaning, usage, isnad, ifadah, hukm, or tanzil.
- The overlap in banned outputs is intentional: both are pre-runtime contract layers under embargo.
- Euclidean Learning audit labels to open runtime domains.
- FailureAlignment to replace `FailureCode`.

## Required Output Shape

Every PR must be scoped to one constitutional objective.
Autonomous work must produce one narrow PR only, then stop.

Each PR must state:

- Scope
- Non-scope
- Authority docs
- Files changed
- Tests run
- Constitutional invariants preserved
- Why this is audit-only

Every new entity must preserve:

- frozen dataclass if in src
- `trace_ref`
- `rank = "CANDIDATE"`
- `residuals`
- named `FailureCode` on rejection
- no I/O in pure source code

## Required Validation

Before finishing any PR, run or state inability to run:

```bash
pytest tests/
pytest tests/test_kpi_indicators.py -v
python -m ci.constitutional_guard --source-dir src
```

## PR Sequencing Law

You may proceed through multiple PRs autonomously only if each PR is small and one-goal.

After each PR, verify:

- no runtime embargo breach
- no forbidden file introduced
- no rank promotion
- no manual computed verdict
- no Boolean proof
- no domain opening

If any invariant fails, stop and report `BLOCKED`.

## Current Roadmap After PR #103

Source of truth: `docs/15_PROJECT_ROADMAP.md`.
Operational companion: `docs/20_AGENT_AUTONOMY_RUNBOOK.md`.

Next-safe-step priority queue:

1. Fix weak or missing tests around computed coverage verdict fixtures.
2. Add negative fixture coverage for allowed contexts so forbidden patterns do not false-positive in authorized documentation.
3. Add schema tests proving `computed_verdict` is rejected for every verdict fixture type.
4. Add manifest tests proving every `expected_verdict` has one positive fixture, at least one unrelated-field negative fixture, and at least one `computed_verdict` rejection fixture.
5. Add canonical family audit fields for `failure_alignment.csv` if absent: `canonical_family`, `domain_scope`, `proof_obligation`, `residual_policy`, `forbidden_runtime_use`; keep all rows `is_executable_row=false` and `executable_mapping=AUDIT_ONLY`.
6. Add or refine agent autonomy instructions/runbook so future Copilot sessions choose the next safe step.
7. Add anti-pattern regression guards for rank promotion, Boolean-as-proof defaults, evidence list as proof, runtime engine names, forbidden runtime artifact names, and coverage matrix artifacts.

Choose one highest-priority safe gap only, prefer docs/schema/data/tests, and stop before runtime/kernel/domain opening.
