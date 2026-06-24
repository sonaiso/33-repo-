# Rejected Runtime Anti-Patterns — `docs/15_REJECTED_RUNTIME_PATTERNS.md`

## Scope
Define forbidden runtime patterns under embargo and keep runtime embargo enforcement audit-only.

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
- `binding_kernel.py` — would introduce runtime kernel before embargo lift.
- `decision_engine.py` — would introduce runtime decision authority before constitutional sequence completion.
- `coverage_matrix_v0.1.yaml` — would convert audit artifacts into runtime coverage authority.
- `BindingDecisionEngine` — would bypass audit-only contracts and open runtime execution paths.
- `MRK boolean defaults` — converts proof obligations into unchecked defaults.
- `domain_proved: true` — boolean-as-proof; proof cannot be asserted by default.
- `unit_proved: true` — boolean-as-proof; proof cannot be asserted by default.
- `identity_preserved: true` — boolean-as-proof; identity preservation requires named checks.
- `trace_preserved: true` — boolean-as-proof; trace continuity requires explicit proof objects.
- `gate_passed: true` — boolean-as-proof; gate status must be derived, not hardcoded.
- `identity_preserved: bool = True` — default-true identity proof bypasses constitutional checks.
- `is_preserved: bool = True` — default-true preservation bypasses constitutional guard conditions.
- `Rank.CERTIFICATE` — would violate `rank = "CANDIDATE"` under embargo.
- `Rank.REJECTED` — introduces rank promotion/reclassification outside authorized runtime flow.
- `evidence list as proof` — evidence references are not executable proof.
- `if self.evidence: self.licensed = True` — licensing may not be granted by evidence-list presence.
- `transform(operation: str): pass` — placeholder translators/predicates are runtime-opening stubs.
- `Gate.condition` as free text (`condition: str`) — textual gates are not constitutional proofs.
- `Bridge.translator` as free text (`translator: str`) — textual translators are not authorized runtime contracts.
- `ComputedVerdict` / `computed_verdict` — manual verdict injection is forbidden under embargo.
- `mrk_defaults` with all `true` fields — pre-approving proofs by defaults is forbidden.

## Enforcement law
A rejected pattern may appear only inside this documentation file as a quoted anti-pattern.
It may not appear in `src/`, `schemas/`, or runtime-facing tests.

## Constitutional invariants preserved
- All rows remain audit-only.
- Runtime embargo remains active.
- No kernel.
- No predicates.
- No translators.
- No coverage runtime.
