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
List exact file paths only. No globs.

## 3) Explicit Non-Authorized Artifacts
List runtime artifacts that remain forbidden in this PR.

## 4) Runtime Boundary
State exactly what runtime surface is requested. If none, say `none`.

## 5) Domain Boundary
State `none` or exactly one domain identifier being opened by this lift request.

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

## 8) Rollback Plan
Required and executable rollback steps.

## 9) FailureAlignment Impact
State impact on FailureCode families and why alignment remains preserved.

## 10) Coverage Schema Impact
State schema-only changes (if any) and confirm no runtime coverage runner is introduced.

## 11) Rank Ceiling Policy
Must remain `CANDIDATE_ONLY` unless a future constitutional protocol explicitly changes it.

## 12) Explicit Non-Blanket Statement
Required statement:
- This lift request authorizes only the exact artifacts listed in this PR.
- All non-listed runtime artifacts remain blocked.
- Readiness/DONE is not lift.
- This template does not authorize runtime.
