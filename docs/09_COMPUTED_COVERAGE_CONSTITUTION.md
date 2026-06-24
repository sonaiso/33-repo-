# Computed Coverage Schema Constitution — `docs/09_COMPUTED_COVERAGE_CONSTITUTION.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5`, `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`, and `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`.

## Scope

PR #76 defines a schema-only, audit-only shape for future coverage cases.
It defines case structure only.
It does not compute verdicts.
It does not authorize runtime.

## Non-scope

No runtime kernel.
No decision engine.
No `coverage_matrix_v0.1.yaml`.
No coverage runner.
No computed verdict logic.
No runtime predicates or translators.
No runtime-domain opening.

## Coverage Schema-Only Law

The schema may declare `expected_verdict` only.
It may not accept manual `computed_verdict`, manual dashboards, MRK boolean defaults, or authoritative runtime claims.

Quoted legacy guard markers retained solely as schema-only prohibitions:
- `ComputedVerdict cannot be manually supplied.` Schema-only interpretation: `computed_verdict` is forbidden.
- `Dashboard must be computed.` Schema-only interpretation: `manual_dashboard` is forbidden, and no dashboard computation is authorized here.
- `YAML may declare expected_verdict only.` Schema-only interpretation: future case data may declare `expected_verdict` only.
- `MRK defaults cannot be all true.` Schema-only interpretation: `mrk_defaults` and Boolean-as-proof fields are forbidden.

## Required Separation

Coverage artifacts must distinguish:
- expected_verdict
- computed_verdict
- test_result

Only `expected_verdict` is allowed in schema-only coverage cases before explicit Runtime Embargo lift.
`computed_verdict` and `test_result` are future computed outputs and must not be manually supplied.

## Allowed Coverage Case Fields

The schema-only coverage case may contain only:

- `case_id`
- `input_text`
- `source_domain`
- `target_domain`
- `source_contract`
- `target_contract`
- `expected_verdict`
- `required_bridges`
- `required_proof_kinds`
- `expected_failure_family`
- `expected_residual_policy`
- `forbidden_outputs`
- `trace_ref`

## Forbidden Coverage Case Fields and Claims

The schema must reject:

- `computed_verdict`
- `manual_dashboard`
- `mrk_defaults`
- `domain_proved`
- `unit_proved`
- `identity_preserved`
- `trace_preserved`
- `gate_passed`
- `is_preserved`
- `rank = CERTIFICATE`
- `rank = REJECTED`
- `authoritative = true`

## Conditional Expected Verdict Requirements

- `EXPECTED_BLOCKED` requires `expected_failure_family`.
- `EXPECTED_RESIDUAL` requires `expected_residual_policy`.
- `EXPECTED_BRIDGE_REQUIRED` requires non-empty `required_bridges`.
- `EXPECTED_PROOF_REQUIRED` requires non-empty `required_proof_kinds`.

## Files changed

- `docs/09_COMPUTED_COVERAGE_CONSTITUTION.md`
- `schemas/coverage_case.schema.json`
- `tests/test_computed_coverage_schema.py`

## Tests run

Required before finishing:

- `pytest tests/`
- `pytest tests/test_kpi_indicators.py -v`
- `python -m ci.constitutional_guard --source-dir src`

## Constitutional invariants preserved

- Runtime Embargo remains active.
- All outputs are schema-only and audit-only.
- No runtime kernel.
- No decision engine.
- No coverage matrix runtime.
- No coverage runner.
- No runtime predicates.
- No runtime translators.
- No rank promotion.
- No Boolean-as-proof.
- No manual computed verdict.
- No runtime domain opening.
