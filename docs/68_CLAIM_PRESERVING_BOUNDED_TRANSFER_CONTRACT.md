# Claim-Preserving Bounded Transfer Contract — `docs/68_CLAIM_PRESERVING_BOUNDED_TRANSFER_CONTRACT.md`

## Constitutional claim (single-goal scope)
Define an audit-only contract that separates bounded checking completeness from intended-class transfer obligations for claim-wise reasoning.

## Selected next-safe-step queue item
- Queue item `9`: anti-pattern guardrails, forbidden-pattern drift tests, instruction/runbook hardening, and audit-only registry/schema hardening only.

## Current constitutional bounds
- L0 is closed.
- L1 work is contract/audit bounded.
- L2 and L3 are locked.
- Runtime embargo remains active.

## Scope
- Define and separate: `MC_n`, `RA_{n,psi}`, `CandComp_U`, `CtxComp_Gamma`, `ChkSound`, `ChkComp`.
- Record the bounded-to-intended transfer condition as claim-wise and counterexample-type-aware.
- Preserve audit-only posture; no executable runtime behavior.

## Non-scope
- No runtime kernel or decision authority.
- No `binding_kernel.py`, `decision_engine.py`, or `coverage_matrix_v0.1.yaml` changes.
- No runtime predicates/translators.
- No computed-verdict runtime.
- No domain opening and no locked-layer opening.

## Authority docs
- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/15_PROJECT_ROADMAP.md`
- `docs/20_AGENT_AUTONOMY_RUNBOOK.md`

## Files changed
- `docs/68_CLAIM_PRESERVING_BOUNDED_TRANSFER_CONTRACT.md`
- `tests/test_claim_preserving_bounded_transfer_contract.py`

## Tests run
- `pytest tests/test_claim_preserving_bounded_transfer_contract.py -v`
- `pytest tests/`
- `pytest tests/test_kpi_indicators.py -v`
- `python -m ci.constitutional_guard --source-dir src`

## Constitutional invariants preserved
- Runtime embargo remains active.
- No runtime authority is introduced.
- No rank promotion is introduced.
- No manual computed verdict is introduced.
- No Boolean-as-proof fields are introduced.
- No domain opening is introduced.

## Why this is audit-only
This contract defines proof obligations and failure taxonomy for documentation and guard tests only. It does not authorize runtime evaluation, runtime transfer engines, or runtime verdict computation.

## Separation law: four non-mergeable layers
`Model != Realization != Context != IntendedClass`

- `Model`: member of `Mod_Sigma`.
- `IntendedClass`: `K subseteq Mod_Sigma` fixed by explicit assumptions.
- `Realization`: witness relation inside a model (`r ||-_{M} B`) and not a new model universe.
- `Context`: context language element (`K[-] in Gamma`) and not a model.

## Contract vocabulary
- `MC_n`: bounded enumeration/checking completeness over `F_n = { M in K_fin : |M| <= n }`.
- `RA_{n,psi}`: `forall M in K, exists N in F_n: M equiv_psi N`.
- `CandComp_U`: candidate-grammar adequacy for extractor search space only.
- `CtxComp_Gamma`: context-language adequacy for contextual distinction only.
- `ChkSound`: `Check(N, psi)=PASS => N models psi`.
- `ChkComp`: `N models psi => Check(N, psi)=PASS`.

## Central transfer law (audit-only theorem shape)
Bounded-to-Intended transfer for a claim `psi` requires all of:
- `RA_{n,psi}`.
- claim-preserving equivalence (`EP`): `M equiv_psi N => (M models psi <=> N models psi)`.
- checker soundness on the bounded fragment.
- exhaustive PASS over required representatives in `F_n`.

Then:
`forall M in K: M models psi`.

## Counterexample-type preservation law
For diagnostic-grade falsification, transfer must preserve counterexample type:
- `M equiv_psi N and M not models psi => CEType(M, psi) = CEType(N, psi)`.

Claim-wise small countermodel obligation is typed:
- `SCM_{psi,tau}(N)`: if a `tau`-typed countermodel exists in `K`, then one exists with size `<= N`.

## Methodological asymmetry law
- Refutation needs one intended countermodel.
- Finite verification of a universal claim needs representation adequacy (`RA_{n,psi}`).

## Failure taxonomy (non-collapsible)
- `MC_n` failure: bounded model exists but was not enumerated/checked.
- `RA` failure: intended model has no claim-preserving bounded representative.
- `CandComp` failure: admissible realization outside candidate grammar.
- `CtxComp` failure: distinguishing context outside `Gamma`.
- `ChkSound` failure: checker returns PASS for a model violating the claim.

## Stability status law
Finite stability is evidence, not cutoff proof.
`EmpiricalStability(i,j)` does not imply `Cutoff_psi`.

## Cutoff legitimacy law
A cutoff is valid only as a representation theorem result:
`Cutoff_psi = N` iff every intended model has a `psi`-equivalent representative of size `<= N`.

Finite quotient count alone is insufficient; finite representatives are also required.
