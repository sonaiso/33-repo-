# Runtime Embargo Lift Protocol — `docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md`

## Scope
Define Runtime Embargo Lift Protocol governance only.

## Non-scope
No `binding_kernel.py`, no `decision_engine.py`, no `coverage_matrix_v0.1.yaml`, no runtime predicates/translators, no computed verdict runtime, no runtime source changes in `src/`, and no automatic opening of `LEXICAL_MADLUL`, `RELATION`, `IFADAH`, `HUKM`, or `TANZIL`.

## Authority docs
- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/15_PROJECT_ROADMAP.md`
- `docs/17_RUNTIME_EMBARGO_READINESS_LEDGER.md`

## Files changed
- `docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md`
- `tests/test_runtime_embargo_lift_protocol.py`

## Tests run
- `pytest tests/test_runtime_embargo_lift_protocol.py -v`
- `pytest tests/`
- `pytest tests/test_kpi_indicators.py -v`
- `python -m ci.constitutional_guard --source-dir src`

## Constitutional invariants preserved
- Runtime Embargo remains active after this PR.
- This PR does not grant runtime execution authority.
- Kernel is not authorized.
- Decision engine is not authorized.
- Coverage matrix runtime is not authorized.

## Protocol claims
Readiness is not lift.
DONE in readiness ledger is not lift.
Only explicit Runtime Embargo Lift PR may authorize runtime.
Implicit lift is forbidden.
Partial/blanket lift is forbidden.
Lift PR must name exact authorized artifacts/files.
Lift PR must include rollback plan.
Lift PR must include negative tests.
Lift does not auto-open LEXICAL_MADLUL/RELATION/IFADAH/HUKM/TANZIL.

## Mandatory negative-test set for any Runtime Embargo Lift PR
- `Rank.CERTIFICATE`
- `Rank.REJECTED`
- `domain_proved: true`
- `unit_proved: true`
- `identity_preserved: true`
- `trace_preserved: true`
- `gate_passed: true`
- `is_preserved: true`
- evidence list as proof
- domain opening without bridge

## Lift authorization boundary
No implicit lift by DONE status.
No implicit lift by passing tests.
No implicit lift by agent approval.
No implicit lift by user delegation/authorization.
No partial or blanket runtime opening.
A lift PR must explicitly list exact files/artifacts it authorizes, and all non-listed artifacts remain blocked.

## Lift types registry (protocol-only)
- `LIFT_TYPE_SCHEMA_RUNTIME` = NOT_AUTHORIZED
- `LIFT_TYPE_PROOF_EVALUATOR` = NOT_AUTHORIZED
- `LIFT_TYPE_BRIDGE_EVALUATOR` = NOT_AUTHORIZED
- `LIFT_TYPE_COVERAGE_RUNNER` = NOT_AUTHORIZED
- `LIFT_TYPE_KERNEL` = NOT_AUTHORIZED

## Constitutional conclusion
Runtime Embargo remains active.
This PR defines authorization protocol only; it does not grant runtime execution authority.
`binding_kernel.py` remains forbidden unless explicitly authorized by a Runtime Embargo Lift PR.
