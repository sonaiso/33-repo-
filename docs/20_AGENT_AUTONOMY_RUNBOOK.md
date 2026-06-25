# Agent Autonomy Runbook — `docs/20_AGENT_AUTONOMY_RUNBOOK.md`

Origin: `docs/00_MAQOOL_CONSTITUTION.md`; `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`; `docs/00B_AGENT_BINDING_CONSTITUTION.md`; `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`

## Scope

This runbook defines constitutionally bounded Copilot autonomy.
It permits an agent to inspect the repository, select the smallest safe next hardening step, complete exactly one narrow PR, and stop at the first constitutional boundary.

## Non-scope

This runbook does not authorize runtime.
It does not authorize a kernel, decision engine, coverage matrix, computed verdict runtime, runtime predicates, runtime translators, rank promotion, or runtime domain opening.
It does not make Euclidean Learning authoritative.
It does not allow FailureAlignment artifacts to replace `FailureCode`.

## Authority docs

- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/00B_AGENT_BINDING_CONSTITUTION.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/15_REJECTED_RUNTIME_PATTERNS.md`

## Current constitutional state

- Runtime Embargo is active.
- L0 is closed.
- L1 work remains contract/audit bounded.
- L2 and L3 remain locked until explicit authorization.
- Euclidean Learning is `AUDIT_SANDBOX_ONLY`.
- FailureAlignment is `AUDIT_ONLY`.
- All constitutional entities remain `rank = "CANDIDATE"` unless a future authorized constitution explicitly changes that rule.

## Hard prohibitions

An autonomous agent must not create, modify, or route around:

- `binding_kernel.py`
- `decision_engine.py`
- `coverage_matrix_v0.1.yaml`

An autonomous agent must not introduce:

- `Rank.CERTIFICATE`
- `Rank.REJECTED`
- `ExecutionRank.CERTIFIED` as runtime authority
- Boolean-as-proof defaults or fields
- evidence list as proof
- identity preservation defaulting to true
- runtime predicates
- runtime translators
- manual `ComputedVerdict`
- computed verdict runtime
- runtime domain opening

## Next-safe-step selection

When assigned a broad hardening request, the agent must:

1. Inspect current docs, tests, schemas, registries, and relevant source contracts.
2. Prefer unresolved review comments or failing tests if they are inside the current constitutional scope.
3. Otherwise choose the highest-priority safe gap that preserves Runtime Embargo.
4. Keep the change to one constitutional objective.
5. Add tests or schema checks that make the guard durable.
6. Avoid unrelated cleanup.
7. Stop after one narrow PR.

Allowed next-safe-step categories include:

- strengthening audit-only forbidden-pattern registries
- adding fixture coverage for guard behavior
- documenting agent-safe workflow boundaries
- adding schema-only constraints that do not compute verdicts
- refining L1 contract documentation without opening runtime

## Stop conditions

The agent must stop and report `BLOCKED` if the next required step needs:

- runtime authorization
- a kernel
- a decision engine
- a coverage matrix runtime
- runtime predicates or translators
- rank promotion
- L2, L3, or runtime domain opening
- Boolean-as-proof
- Euclidean Learning authority beyond `AUDIT_SANDBOX_ONLY`
- FailureAlignment replacement of `FailureCode`

## Required PR body shape

Every PR produced under this runbook must state:

- Scope
- Non-scope
- Authority docs
- Files changed
- Tests run
- Constitutional invariants preserved

## Required validation

Before finishing, run or state inability to run:

```bash
pytest tests/
pytest tests/test_kpi_indicators.py -v
python -m ci.constitutional_guard --source-dir src
```

Focused tests may be run first, but they do not replace the required validation list unless the agent clearly states why full validation could not run.

## Constitutional invariants preserved

- Runtime embargo remains active.
- No runtime kernel.
- No decision engine.
- No coverage matrix.
- No runtime predicates.
- No runtime translators.
- No rank promotion.
- No Boolean-as-proof.
- No manual computed verdict.
- No runtime domain opening.
- Euclidean Learning remains audit-only.
- FailureAlignment remains audit-only.
