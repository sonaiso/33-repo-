# Rejected Runtime Anti-Patterns — `docs/15_REJECTED_RUNTIME_PATTERNS.md`

## Scope
Define forbidden pre-runtime implementation patterns and keep runtime embargo enforcement audit-only.

## Non-scope
This document does not authorize kernel code, predicates, translators, computed runtime coverage, or any runtime-domain opening.

## Authority docs
- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `.github/copilot-instructions.md`

## Rejected patterns (embargoed)
- `binding_kernel.py`
- `decision_engine.py`
- `coverage_matrix_v0.1.yaml`
- `BindingDecisionEngine`
- `MRK boolean defaults`
- `domain_proved: true`
- `unit_proved: true`
- `identity_preserved: true`
- `trace_preserved: true`
- `gate_passed: true`
- `is_preserved: bool = True`
- `Rank.CERTIFICATE`
- `Rank.REJECTED`
- `evidence list as proof`
- `transform(operation: str): pass`

## Constitutional invariants preserved
- All rows remain audit-only.
- Runtime embargo remains active.
- No kernel.
- No predicates.
- No translators.
- No coverage runtime.
