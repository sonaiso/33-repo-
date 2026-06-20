# Runtime Embargo Constitution — `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5`, `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`, and PR #37 (`D1_DAL_ONLY → D2_LAFZI_FORM` declarative bridge-spec only).

## Embargo Rule (PR #38)
Runtime remains embargoed.
Runtime prerequisites before embargo lift:
1. D1_DAL_ONLY contracts are frozen.
2. D2_LAFZI_FORM contracts are frozen.
3. DalToLafziBridgeSpec is declared.
4. FailureAlignment is audit-clean.
5. ProofObject references have stable failure policies.
6. No Boolean-as-proof remains in proposed runtime specs.
7. No Rank.CERTIFICATE exists in L1.
8. No manual computed verdict exists.

## Explicit Prohibitions Before Embargo Lift
- binding_kernel.py is forbidden before embargo lift.
- decision_engine.py is forbidden before embargo lift.
- coverage_matrix_v0.1.yaml is forbidden before computed coverage schema.
- Runtime predicates and runtime translators are forbidden in this phase.
- L1 output rank remains `CANDIDATE` only.

## Constitutional Sequence
Domain → Contract → BridgeSpec → ProofObject → FailureAlignment → Kernel.
