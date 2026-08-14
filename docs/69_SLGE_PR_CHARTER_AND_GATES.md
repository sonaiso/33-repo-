# 69 — SLGE PR Charter + Migration Certificate + PR Acceptance Gates (Audit-Only)

## One-Goal Constitutional Claim

Produce one audit-only operational charter that converts the proposed sequence (`PR-0` to `PR-5`) into a reusable execution template with explicit constitutional boundaries.

## Governing Authority Docs

- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/15_PROJECT_ROADMAP.md`
- `docs/20_AGENT_AUTONOMY_RUNBOOK.md`

## Constitutional Bounds (Restated)

- L0 is closed.
- L1 is contract/audit bounded.
- L2 and L3 are locked.
- Runtime embargo is active.
- Euclidean Learning remains `AUDIT_SANDBOX_ONLY`.

## Selected Next-Safe-Step Queue Item

- Queue item `#9`: instruction/runbook hardening and audit-only guardrail reinforcement.

## Scope

- Define a short PR charter for `PR-0` through `PR-5`.
- Preserve strict separation intent: `meta`, `formation`, `elab`, `erg`, `reality`, `domains`, `runtime`.
- Provide a fillable `Migration Certificate` template.
- Provide a fillable `PR Acceptance Gates` template.

## Non-Scope

- No runtime kernel or runtime admission implementation.
- No changes to `binding_kernel.py`, `decision_engine.py`, or `coverage_matrix_v0.1.yaml`.
- No L2/L3 opening.
- No rank promotion, no computed-verdict runtime, no domain opening.

## PR Charter (PR-0 to PR-5)

| PR | Objective | Required Output | Hard Boundary |
|---|---|---|---|
| PR-0 | Skeleton + constitutions + dependency law + CI boundary tests | repository skeleton docs/contracts and import-boundary CI checks | no runtime/domain execution |
| PR-1 | Minimal meta candidate + deletion tests | minimal `meta` candidate primitives and deletion tests | no hidden primitive promotion |
| PR-2 | Reconstruction/deletion attacks + derivability report | derivability verdict per candidate primitive | no runtime semantics |
| PR-3 | Fractal formation on toy + countermodels | toy substrate closure/lift/across/reopen checks with countermodels | no domain-specialized assumptions |
| PR-4 | ELAB foundation (no truth/agents) | lineage/support/entitlement audit contracts and tests | `ELAB -> Truth` and `ELAB -> Agent` forbidden |
| PR-5 | ELAB adversarial suite + conservation baseline | adversarial lineage/rank tests and conservation baseline | no reality/runtime authority |

## Early Success Criteria (Before Arabic)

- No `meta` changes are required when swapping `toy` / `arithmetic` / `causality` substrates.
- ELAB passes adversarial lineage cases.
- Any rank claim fails automatically when valid supports or traceable lineage are missing.

## Template A — Migration Certificate

Use one certificate per migrated legacy artifact. Migration is blocked if any mandatory field is missing.

```md
# Migration Certificate (MC)

## Identity
- MC ID:
- Date:
- Owner:

## Artifact Mapping
- OldArtifact:
- SourceRepository:
- SourcePath:
- ProposedNewLocation:

## Law Extraction
- LawExtracted:
- WhyLawIsGeneral (not domain-bound):
- ConstitutionalTraceRef:

## Dependency Audit
- Dependencies:
- HiddenPrimitivesAudit:
- RuntimeCouplingCheck:

## Classification
- Decision: Migrate | Reconstruct | Revalidate | Archive
- Justification:

## Regression Witness
- RegressionWitnessCaseIDs:
- PositiveCases:
- NegativeCases:
- Residual/BlockedCases:

## Security + Embargo Checks
- IntroducesRuntimeAuthority: yes/no
- IntroducesComputedVerdictRuntime: yes/no
- IntroducesRankPromotion: yes/no
- OpensLockedLayer: yes/no

## Validation
- TestsRun:
- Result:

## Approval
- Reviewer:
- Status: APPROVED | REJECTED | BLOCKED
- Notes:
```

## Template B — PR Acceptance Gates

Every PR must pass all gates before merge.

```md
# PR Acceptance Gates

## Gate 0 — One Goal Only
- [ ] Single constitutional objective is explicitly stated
- [ ] Scope is explicit
- [ ] Non-scope is explicit

## Gate 1 — Constitutional Authority
- [ ] Authority docs are listed
- [ ] Constitutional bounds are restated
- [ ] Queue item selection is explicit

## Gate 2 — Architecture Boundary
- [ ] No forbidden import direction introduced
- [ ] No runtime/kernel/decision authority introduced
- [ ] No locked-layer opening

## Gate 3 — Evidence and Traceability
- [ ] Every new claim maps to tests or fixtures
- [ ] Failure paths are explicit and named
- [ ] Lineage/traceability is test-visible

## Gate 4 — Regression Safety
- [ ] Positive coverage exists for intended behavior
- [ ] Negative coverage exists for forbidden behavior
- [ ] Residual/blocked behavior is covered

## Gate 5 — Required Validation
- [ ] `pytest tests/`
- [ ] `pytest tests/test_kpi_indicators.py -v`
- [ ] `python -m ci.constitutional_guard --source-dir src`

## Gate 6 — Audit-Only Invariants
- [ ] Runtime embargo preserved
- [ ] No forbidden files added/modified
- [ ] No rank promotion
- [ ] No computed-verdict runtime
- [ ] No Boolean-as-proof introduction

## Final Verdict
- [ ] PASS
- [ ] BLOCKED (state blocker and constitutional reason)
```

## Why This Is Audit-Only

This artifact introduces no executable runtime behavior. It defines governance templates, sequencing, and merge gates only.
