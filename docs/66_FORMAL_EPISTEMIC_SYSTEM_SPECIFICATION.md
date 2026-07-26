# Formal Epistemic System Specification — `docs/66`

## المواصفة الصورية للمنظومة المعرفية — Audit Only

## Authority

- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/15_PROJECT_ROADMAP.md`
- `docs/20_AGENT_AUTONOMY_RUNBOOK.md`
- `docs/21_LICENSED_INTELLIGIBILITY_CHAIN_CONSTITUTION.md`

## Constitutional Status

This document is an audit-only formal contract. It specifies epistemic entities and
licensed transitions without creating runtime authority.

```text
Runtime status: AUDIT_ONLY
L0 is closed.
L1 is contract/audit bounded.
L2 remains locked.
L3 remains locked.
Runtime embargo remains active.
```

## One Auditable Claim

`TheorySystem` and `Macro-JRC` must be treated as different formal objects:

- `TheorySystem` is a structured epistemic object.
- `Macro-JRC` is a readiness predicate over that object.

Internal closure is not external match.

## Scope

- Define formal signatures for proposition, network, theory system, validation.
- Define typed macro-relations and licensing predicates.
- Define partial transition functions `f_8`, `f_9`, `f_10`, `f_11`.
- Preserve identity, rank-boundedness, residual visibility, and no-leap constraints.
- Record anti-pattern laws that block invalid epistemic jumps.

## Non-scope

This document does not:

- create a runtime kernel;
- create a decision engine;
- create a coverage matrix runtime;
- create runtime predicates or translators;
- compute runtime verdict authority;
- open `L2`;
- open `L3`;
- open any runtime domain;
- promote rank above `CANDIDATE`;
- replace `FailureCode` with FailureAlignment artifacts.

## Signature and Sorts

Let:

- `J`: set of propositions.
- `N`: set of networks.
- `T`: set of theory systems.
- `AxiomSet`: powerset candidates of proposition subsets.
- `M_R`: set of typed macro-relation kinds.
- `ValidationMode`: `{FORMAL_PROOF, EMPIRICAL_TEST, INTERPRETIVE_COHERENCE, NORMATIVE_JUSTIFICATION, COMPUTATIONAL_VERIFICATION, INSTITUTIONAL_VALIDATION}`.
- `ValidationResult`: `{TRUE, FALSE, UNDETERMINED}`.
- `MatchResult`: `{PROVEN_MATCH, UNPROVEN_MATCH, PROVEN_MISMATCH, UNFIT}`.

Auxiliary predicates and operators:

- `LicensedRel(p_i, p_j, r)`.
- `DomainOf(p)` and `CompatibleDomain(d1, d2)`.
- `Blocking(ResidualSet)`.
- `InternallyClosed(N)`.
- `TheoryReady(T)` (alias for `Macro-JRC(T)`).

## Formal Objects

### Proposition (`p ∈ J`)

```text
p = <id_p, S_p, P_p, L_p, Pol_p, Sc_p, D_p, T_p, M_p, F_p, R_p, Ω_p, Tr_p>
Identity(p) = id_p
```

Identity is stable; theoretical role is external:

```text
RoleWithinTheory(p, τ) is relation metadata, not proposition identity.
```

### Network (`n ∈ N`)

```text
n = <P_n, E_n>
P_n ⊆ J
E_n ⊆ P_n × P_n × M_R
Identity(n) = { id_p | p ∈ P_n }
```

A network is invalid if it has no typed edges:

```text
∀P ⊆ J: <P, ∅> ∉ N
```

### Typed Macro-Relations (`M_R`)

```text
M_R = M_R^logical ∪ M_R^proof ∪ M_R^explanatory ∪ M_R^empirical ∪ M_R^domain ∪ M_R^historical
```

```text
M_R^logical     = {ENTAILS, EQUIVALENT, CONTRADICTS, CONSISTENT_WITH}
M_R^proof       = {DERIVES_FROM, REQUIRES, DISCHARGES, USES}
M_R^explanatory = {EXPLAINS, IS_EXPLAINED_BY}
M_R^empirical   = {SUPPORTS, UNDERDETERMINES, FALSIFIES, FITS_WITHIN_ERROR}
M_R^domain      = {GENERALIZES, SPECIALIZES, OVERLAPS, EXCLUDES}
M_R^historical  = {INFLUENCES, IS_REVISED_BY, SUPERSEDES}
```

Every edge must satisfy:

```text
e = <p_i, p_j, r> ∈ E_n  ⇒  r ∈ M_R ∧ LicensedRel(p_i, p_j, r)
```

### Theory System (`τ ∈ T`)

```text
τ = <n, A, I, V, D, O, G, ρ, ε, Tr>
A ⊆ P_n
Identity(τ) = <O, D, CoreInvariants(τ)>
```

`A` means non-derived inside the same system, not evidence-free absolutely.

### Macro-JRC (`TheoryReady`)

`Macro-JRC` is a predicate, not an ontology object:

```text
Macro-JRC(τ) ⇔
  InternalConsistency(τ)
  ∧ DomainDeclared(τ)
  ∧ ValidationModeDeclared(τ)
  ∧ ¬Blocking(ε_τ)
  ∧ AllAxiomsLicensed(τ)
  ∧ AllInferenceRulesLicensed(τ)
  ∧ AllNetworkRelationsTypedAndLicensed(τ)
```

## Validation and External Match

```text
Validate(τ, mode) ∈ ValidationResult
```

```text
Match(τ, E, D) is TRUE only when:
Validate(τ, mode) = TRUE
and Evidence(E) is sufficient and domain-appropriate.
```

Internal closure never implies external match:

```text
Macro-JRC(τ) ⇏ Match(τ, E, D)
```

## Licensed Transition Functions

### `f_8`: propositions to network

```text
f_8 : J × J × M_R ⇀ N
```

```text
f_8(p_1, p_2, r) =
  <{p_1, p_2}, {<p_1, p_2, r>}>
  if LicensedRel(p_1, p_2, r)
     ∧ CompatibleDomain(DomainOf(p_1), DomainOf(p_2))
     ∧ RankBoundedByInputs
     ∧ ¬Blocking(Ω_p1 ∪ Ω_p2 ∪ Ω_r)
  undefined otherwise
```

Invariants:

```text
Identity(f_8(...)) = {id_p1, id_p2}
Residuals(f_8(...)) = Ω_p1 ∪ Ω_p2 ∪ Ω_r
```

### `f_9`: network to theory system

```text
f_9 : N × AxiomSet × I × D × O ⇀ T
```

```text
f_9(n, A, I, D, O) =
  <n, A, I, Vocab(n), D, O, G_0, ρ_0, ε_0, Tr_0>
  if A ⊆ P_n
     ∧ RulesCompatible(I, D, O)
     ∧ DomainDeclared(D)
     ∧ OntologyDeclared(O)
     ∧ InternallyClosed(n)
  undefined otherwise
```

Where:

```text
ρ_0 = max({Rank(p) | p ∈ P_n})
ε_0 inherits residuals from propositions and edges and records construction residuals.
```

### `f_10`: macro readiness certificate

```text
f_10 : T → {TRUE, FALSE} × Residuals × Trace
```

```text
f_10(τ) =
  (TRUE,  ∅,              Tr(τ)) if Macro-JRC(τ)
  (FALSE, ε_blocking(τ),  Tr(τ)) otherwise
```

### `f_11`: theory to match outcome

```text
f_11 : T × ValidationMode × EvidenceSet → MatchResult
```

Deterministic result mapping:

- incompatible mode with `D` -> `UNFIT`
- mode compatible and `Validate = TRUE` with sufficient evidence -> `PROVEN_MATCH`
- mode compatible and `Validate = FALSE` with sufficient counter-evidence -> `PROVEN_MISMATCH`
- otherwise -> `UNPROVEN_MATCH`

## Anti-Pattern Laws

- `Order(p_1, p_2) ⇏ ENTAILS(p_1, p_2)`.
- `Identity(p) ≠ RoleWithinTheory(p, τ)`.
- Internal consistency is not empirical proof.
- Readiness certificate is not final reasonableness verdict.

## Reopen Law (Directed Reopen)

```text
Reopen(x) = { y | DependsOn(y, x) in dependency graph }
```

Only downstream dependents are reopened.

## Audit Output Shape for This Spec Family

Any future update based on this document must report:

- Scope.
- Non-scope.
- Authority docs consulted.
- Files changed.
- Tests run.
- Constitutional invariants preserved.
- Why the change is audit-only.

## Constitutional Invariants Preserved

- Runtime embargo remains active.
- No runtime kernel.
- No decision engine.
- No coverage matrix runtime.
- No runtime predicates/translators.
- No rank promotion.
- No runtime domain opening.
- FailureAlignment remains audit-only.

## Why This Is Audit-Only

This specification defines contracts, predicates, and invariants for epistemic
reasoning structure. It does not grant execution authority, runtime decision
power, or locked-layer opening.
