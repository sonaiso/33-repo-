# Rejected Runtime Anti-Patterns — docs/15_REJECTED_RUNTIME_PATTERNS.md

Origin: `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`; `docs/00_MAQOOL_CONSTITUTION.md`

## Scope

PR #63 records rejected runtime anti-patterns and guardrails while the Runtime Embargo remains active.

## Non-scope

This document is not an implementation plan.
It does not authorize runtime, a kernel, predicates, translators, coverage runners, computed verdicts, or runtime-domain opening.

## Authority docs

Derived from:

- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/16_PROOF_FAILURE_POLICY_ALIGNMENT.md`

## Status

This document records rejected patterns only.
It is audit-only.
It is not an implementation plan.
It does not authorize runtime.

## Rejected Artifacts

The following files are forbidden before explicit Runtime Embargo lift:

- `binding_kernel.py`
- `decision_engine.py`
- `coverage_matrix_v0.1.yaml`

## Rejected Rank Patterns

Forbidden:

- `Rank.CERTIFICATE`
- `Rank.REJECTED`
- ExecutionRank.CERTIFIED as runtime authority

Required:

- `rank = "CANDIDATE"`

## Rejected Boolean Proof Patterns

Forbidden:

- `domain_proved: true`
- `unit_proved: true`
- `identity_preserved: true`
- `trace_preserved: true`
- `gate_passed: true`
- `is_preserved: bool = True`
- `identity_preserved: bool = True`
- `MRK boolean defaults`

Required:

- `MRKProof`
- `IdentityProof`
- `GateProof`
- `BridgeProof`
- `EvidenceProof`
- `CoverageProof`

These are structured proof objects, not Boolean flags.
They must preserve constitutional traceability through `trace_ref`, `rank`, and `residuals`, and they remain non-runtime until explicit embargo lift.

## Rejected Evidence Pattern

Forbidden:

- evidence list as proof
- `if self.evidence: self.licensed = True`

```python
if self.evidence:
    self.licensed = True
```

Required:

Evidence must be `EvidenceProof` or `EvidenceObject` with:

- scope
- rank
- trace
- residuals
- invalidators

## Rejected Gate/Bridge Patterns

Forbidden:

```python
class Gate:
    condition: str

class Bridge:
    translator: str
```

Required:

- `GateSpec` with `predicate_ref`
- `BridgeSpec` with `translator_ref` and `invariant_policy_ref`
- `ProofObject` required before runtime lift

## Rejected SGE Pattern

Forbidden:

- `def transform(self, operation: str): pass`

```python
def transform(self, operation: str):
    pass
```

Required:

- `OperationSpec`
- `GateProof`
- `BridgeProof` if crossing domain

## Rejected Coverage Patterns

Forbidden:

- manual `ComputedVerdict`
- `computed_verdict`
- `mrk_defaults` all true
- YAML granting proof
- dashboard manual totals
- `manual_dashboard`

Required:

- `expected_verdict` only in schema stage
- computed verdict only after explicit runtime authorization

## Enforcement Law

A rejected pattern may appear only inside this documentation file (`docs/15_REJECTED_RUNTIME_PATTERNS.md`) as a quoted anti-pattern, or inside guard tests that tokenize away quoted Python strings before scanning.
It may not appear as executable source, schema authority, runtime configuration, or runtime-facing behavior.

## Files changed

- `docs/15_REJECTED_RUNTIME_PATTERNS.md`
- `tests/test_runtime_antipatterns_embargo.py`

## Tests run

Required before finishing:

- `pytest tests/`
- `pytest tests/test_kpi_indicators.py -v`
- `python -m ci.constitutional_guard --source-dir src`

## Constitutional invariants preserved

- Runtime embargo remains active.
- All outputs are audit-only.
- No runtime kernel.
- No decision engine.
- No coverage runner.
- No runtime predicates.
- No runtime translators.
- No rank promotion.
- No Boolean-as-proof.
- No manual computed verdict.
- No runtime domain opening.
