# TraceStep Identity ProofObject Backing Contract — `docs/18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md`

## Scope
TraceStep identity proof backing contract only.

This document defines the audit contract required before the readiness ledger item
`TraceStep identity ProofObject-backed` may move from `PARTIAL` to `DONE` in a
later implementation PR.

## Non-scope
No runtime kernel, no decision engine, no runtime predicates, no runtime
translators, no coverage runtime, and no ledger promotion to DONE.

This PR is docs/tests-only and does not modify TraceStep runtime behavior.

## Authority docs
- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/08_PROOF_OBJECT_CONSTITUTION.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/15_REJECTED_RUNTIME_PATTERNS.md`
- `docs/17_RUNTIME_EMBARGO_READINESS_LEDGER.md`

## Files changed
- `docs/18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md`
- `tests/test_tracestep_identity_proof_contract.py`

## Tests run
- `pytest tests/`
- `pytest tests/test_kpi_indicators.py -v`
- `python -m ci.constitutional_guard --source-dir src`

## Constitutional invariants preserved
- Runtime Embargo remains active.
- No runtime kernel is authorized.
- No decision engine is authorized.
- No runtime predicates or runtime translators are authorized.
- No coverage runtime is authorized.
- No ledger status is promoted to DONE by this contract.
- No rank above `CANDIDATE` is authorized.
- Boolean fields cannot prove TraceStep identity preservation.

## Contract term
`TraceStepIdentityProofRequirement` is a contract term only.
It is not a new runtime entity, runtime predicate, runtime translator, kernel,
decision engine, or coverage runtime.

## Identity proof backing requirement
TraceStep identity proof is ProofObject-backed only when a future implementation
requires an `IdentityProof` reference or a `ProofObject` reference for identity
continuity.

The future implementation must preserve:
- `trace_ref`
- `rank = "CANDIDATE"`
- `residuals`
- `preserved_identity_refs`
- rejection on identity loss with named `FailureCode`

## Boolean-as-proof rejection
TraceStep identity cannot be proven by Boolean fields.
`identity_preserved=True` cannot prove identity preservation.
`is_preserved=True` cannot prove identity preservation.
Implicit identity preservation is forbidden.

## Ledger status
The current ledger remains:

```text
TraceStep identity ProofObject-backed | PARTIAL | explicit bool only
```

Missing `IdentityProof` or `ProofObject` reference keeps the readiness ledger
status `PARTIAL` until a later implementation PR changes the TraceStep model
with tests.

This PR does not update the runtime ledger to DONE.

## Runtime Embargo
Runtime Embargo remains active.
Kernel is not authorized.
Decision engine is not authorized.
Coverage matrix runtime is not authorized.
