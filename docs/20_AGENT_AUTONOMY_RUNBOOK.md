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
- `docs/15_PROJECT_ROADMAP.md`
- `docs/20_AGENT_AUTONOMY_RUNBOOK.md`

## Current constitutional state

- Runtime Embargo is active.
- L0 is closed.
- L1 work remains contract/audit bounded.
- L2 and L3 remain locked until explicit authorization.
- Euclidean Learning is `AUDIT_SANDBOX_ONLY`.
- FailureAlignment is `AUDIT_ONLY`.
- All constitutional entities remain permanently constrained to `rank = "CANDIDATE"` under the current constitutional law.

## Current hardening baseline

- PR #103 added the `expected_verdict` fixture matrix for computed coverage.
- PR #105 strengthened the computed verdict fixture guardrails after that matrix.
- PR #106 synchronizes autonomy guidance to the post-PR #106 guardrail state and hardens anti-pattern regression guards.
- PR #110 confirms the autonomous agent posture is guardrails-only and audit-only.
- Post-PR #110 autonomy means `Constitution-bound autonomous auditor`.
- Autonomy inside audit. No autonomy inside runtime.
- Rejected runtime examples are anti-patterns, not implementation plans.
- Marker phrase: expected_verdict fixture matrix.
- The PR #103 matrix includes positive fixtures for every `expected_verdict` label.
- PR #105 confirms the matrix includes negative fixtures for irrelevant outcome fields and for `computed_verdict`.
- Computed coverage is schema/fixture based only.
- `expected_verdict` fixtures are declarative only; `computed_verdict` cannot be supplied by fixture data.
- all `computed_verdict` examples remain invalid fixture payloads only.
- Completed computed-verdict fixture work must not be repeated by future autonomy.
- Completed forbidden-pattern fixture coverage must not be repeated when already covered.
- Completed allowed-context negative fixture coverage must not be repeated when already covered.
- do not regress it: future autonomy must build on schema, fixtures, manifests, registries, and audit guardrails.
- Do not convert schema fixtures into runtime cases, computed outcomes, a coverage runner, or runtime readiness.

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
- computed verdict runtime
- runtime domain opening
- `DAL_ONLY` producing root, weight, word, tool, meaning, isnad, ifadah, hukm, or tanzil
- `LAFZI_FORM` producing lexical meaning, usage, isnad, ifadah, hukm, or tanzil
- Euclidean Learning audit labels opening runtime domains
- FailureAlignment replacing `FailureCode`

## Next-safe-step selection

When assigned a broad hardening request, the agent must:

1. Inspect current docs, tests, schemas, registries, and relevant source contracts.
2. Prefer unresolved review comments or failing tests if they are inside the current constitutional scope.
3. Otherwise choose the highest-priority safe gap that preserves Runtime Embargo.
4. Keep the change to one constitutional objective.
5. Add tests or schema checks that make the guard durable.
6. Avoid unrelated cleanup.
7. Stop after one narrow PR.

## Mandatory One-Goal Execution Protocol

Before any implementation step, complete this sequence:

1. Declare one auditable constitutional claim only (single-goal scope, no multi-goal execution).
2. Declare governing authority docs for this task:
   - `docs/00_MAQOOL_CONSTITUTION.md`
   - `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
   - `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
   - `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
   - `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
   - `docs/15_PROJECT_ROADMAP.md`
   - `docs/20_AGENT_AUTONOMY_RUNBOOK.md`
3. Re-state current constitutional bounds: L0 closed, L1 contract/audit bounded, L2/L3 locked, runtime embargo active.
4. Select exactly one queue item from the next-safe-step priority queue.
5. State Scope and Non-scope explicitly to prevent runtime/kernel/decision-authority drift.
6. Produce one verifiable audit-only output and stop.
7. Run required validation commands.
8. If any required next step needs runtime authorization or locked-layer opening, stop and report `BLOCKED`.

Operator prompt (explicit narrow-step trigger):
إذا أردت، أبدأ الآن بالخطوة التالية الضيقة الآمنة (PR واحد فقط) وفق خيارك التالي.

Allowed next-safe-step categories include:

- resolving review comments or weak tests inside the current constitutional scope
- strengthening anti-pattern guardrails
- adding forbidden-pattern drift tests
- hardening instruction/runbook guardrails
- strengthening audit-only forbidden-pattern registries
- adding fixture coverage for guard behavior
- documenting agent-safe workflow boundaries
- adding schema-only constraints that do not compute verdicts
- refining L1 contract documentation without opening runtime

## Highest-priority safe gap queue

After PR #110, select the first narrow gap that still applies:

1. Closed by PR #105: computed coverage verdict fixture tests are strengthened.
2. Closed before this transition: allowed-context negative fixture coverage exists so forbidden patterns do not false-positive in authorized documentation.
3. Closed by PR #105: schema tests prove `computed_verdict` is rejected for every verdict fixture type.
4. Closed by PR #105: manifest tests prove every `expected_verdict` has one positive fixture, at least one unrelated-field negative fixture, and at least one `computed_verdict` rejection fixture; marker phrase: computed_verdict rejection fixture.
5. Closed before this transition: `failure_alignment.csv` has `canonical_family`, `domain_scope`, `proof_obligation`, `residual_policy`, `forbidden_runtime_use`; all rows remain `is_executable_row=false` and `executable_mapping=AUDIT_ONLY`.
6. Closed by PR #106: keep agent autonomy instructions/runbook synchronized with the post-PR #106 guardrail state so future sessions do not repeat completed computed-verdict fixture work.
7. Closed by PR #110: keep post-PR #110 autonomy guardrails audit-only; rejected runtime examples remain anti-patterns, not implementation plans.
8. Current safe gap after PR #110: fix unresolved review comments or weak tests from the latest merged PRs if they stay inside audit-only guardrails.
9. Next safe gaps after PR #110: strengthen anti-pattern guardrails, forbidden-pattern drift tests, instruction/runbook hardening, and audit-only registry/schema hardening only.

Stop after exactly one queue item. If the first remaining queue item would require runtime, a kernel, domain opening, semantic decision authority, rank promotion, Boolean-as-proof, or computed verdict runtime, report `BLOCKED`.

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

- Summary
- Scope
- Non-scope
- Authority docs consulted
- Files changed
- Tests added/changed
- Tests run
- Runtime embargo status
- Constitutional invariants preserved
- Why this is audit-only

## Required validation

Before finishing, run or state inability to run:

```bash
pytest tests/
pytest tests/test_kpi_indicators.py -v
python -m ci.constitutional_guard --source-dir src
```

Focused tests may be run first, but they do not replace the required validation list.
If the execution environment prevents a required command from running, the agent must state the exact command, failure output, and constitutional blocker before finishing.

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
