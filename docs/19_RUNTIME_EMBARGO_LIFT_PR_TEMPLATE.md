# Runtime Embargo Lift PR Template — `docs/19_RUNTIME_EMBARGO_LIFT_PR_TEMPLATE.md`

## Scope
Define mandatory request shape for any future Runtime Embargo Lift PR.

## Non-scope
No runtime lift, no `binding_kernel.py`, no `decision_engine.py`, no `coverage_matrix_v0.1.yaml`, no runtime predicates/translators, no computed verdict runtime, and no automatic domain opening.

## Authority docs
- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/17_RUNTIME_EMBARGO_READINESS_LEDGER.md`
- `docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md`

## Constitutional invariants preserved
- Runtime Embargo remains active.
- Readiness is not lift.
- DONE in readiness ledger is not lift.
- This template does not authorize runtime artifacts.
- No blanket lift is allowed.

## Runtime Embargo Lift PR Template

## 1) Lift Type
One of:
- `LIFT_TYPE_SCHEMA_RUNTIME`
- `LIFT_TYPE_PROOF_EVALUATOR`
- `LIFT_TYPE_BRIDGE_EVALUATOR`
- `LIFT_TYPE_COVERAGE_RUNNER`
- `LIFT_TYPE_KERNEL`

## 2) Exact Authorized Artifacts / Files
List exact repo-relative canonical file paths only.
- No globs/wildcards (`*`, `?`, `[ ]`, `{ }`).
- No absolute paths.
- No `..` segments.
- No `.` segments anywhere in the path.
- No backslashes.
- No empty segments (`//`).
- No trailing slash.
- No leading `./`.
- No leading or trailing whitespace.
- Forbidden runtime paths may not appear in `authorized_artifacts` for any current lift type, including proof evaluator, bridge evaluator, coverage runner, and kernel lift requests.
- Paths must already be canonical; do not rely on normalization/path cleanup to authorize artifacts.

## 3) Explicit Non-Authorized Artifacts
List runtime artifacts that remain forbidden in this PR.
`non_scope_artifacts` in the lift payload must include the full canonical forbidden set.

Minimum forbidden runtime paths:
Source-of-truth (audit-only): `data/forbidden_runtime_artifacts.json`
- `src/taaqqul_slot_geometry/L1/binding_kernel.py`
- `src/taaqqul_slot_geometry/L1/decision_engine.py`
- `src/taaqqul_slot_geometry/runtime/binding_kernel.py`
- `src/taaqqul_slot_geometry/runtime/decision_engine.py`
- `src/taaqqul_slot_geometry/core/binding_kernel.py`
- `src/taaqqul_slot_geometry/core/decision_engine.py`
- `coverage_matrix_v0.1.yaml`
- `docs/coverage_matrix_v0.1.yaml`
- `data/coverage_matrix_v0.1.yaml`
- `schemas/coverage_matrix_v0.1.yaml`
- `tests/test_binding_constraints.py`
- `l_protocol/engine/binding_kernel.py`
- `l_protocol/engine/decision_engine.py`
- `l_protocol/contracts/binding_instructions.py`
- `l_protocol/coverage_matrix_v0.1.yaml`
- `l_protocol/tests/test_binding_constraints.py`

## 4) Runtime Boundary
State exactly what runtime surface is requested. If none, say `none`.

## 5) Domain Boundary
State `none` or exactly one domain identifier being opened by this lift request.

Current embargo rule: `domain_opening` must be `none` for all current lift types:
- `LIFT_TYPE_SCHEMA_RUNTIME`
- `LIFT_TYPE_PROOF_EVALUATOR`
- `LIFT_TYPE_BRIDGE_EVALUATOR`
- `LIFT_TYPE_COVERAGE_RUNNER`
- `LIFT_TYPE_KERNEL`

## 6) Proof Objects Required
List mandatory ProofObject contracts and trace references.

## 7) Negative Tests Required
Must include explicit rejection tests for:
- `Rank.CERTIFICATE`
- `Rank.REJECTED`
- Boolean-as-proof defaults (`domain_proved`, `unit_proved`, `identity_preserved`, `trace_preserved`, `gate_passed`, `is_preserved`)
- evidence-list-as-proof
- domain opening without bridge
- manually supplied computed verdict

Canonical forbidden anti-pattern signatures are audit-only and governed by
`data/forbidden_runtime_patterns.json`; this reference does not authorize runtime.

Minimum required negative-test identifiers:
- `reject-rank-certificate`
- `reject-rank-rejected`
- `reject-boolean-as-proof`
- `reject-evidence-list-as-proof`
- `reject-domain-open-without-bridge`
- `reject-manual-computed-verdict`

## 8) Rollback Plan
Required and executable rollback steps.

## 9) Readiness Ledger Residuals Acknowledgement
Required fields in the lift request payload:
- `readiness_ledger_source: docs/17_RUNTIME_EMBARGO_READINESS_LEDGER.md`
- `residual_blockers_acknowledged: true`

This acknowledgement is mandatory and does not authorize runtime by itself.

## 10) FailureAlignment Impact
State impact on FailureCode families and why alignment remains preserved.

## 11) Coverage Schema Impact
State schema-only changes (if any) and confirm no runtime coverage runner is introduced.

## 12) Rank Ceiling Policy
Must remain `CANDIDATE_ONLY` unless a future constitutional protocol explicitly changes it.

## 13) Explicit Non-Blanket Statement
Required statement:
- This lift request authorizes only the exact artifacts listed in this PR.
- All non-listed runtime artifacts remain blocked.
- Readiness/DONE is not lift.
- This template does not authorize runtime.
