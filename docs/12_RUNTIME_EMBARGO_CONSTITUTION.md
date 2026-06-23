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

## Euclidean Learning Exception Boundary
- `core/euclidean_learning.py` is permitted only as an isolated audit sandbox under active embargo.
- Euclidean learning outputs are audit-only and are never authoritative system decisions.
- Euclidean learning does not replace `binding_kernel.py` and cannot implement `decision_engine.py`.
- Euclidean learning labels do not open runtime domains:
  - `T11_RELATION_AUDIT` does not open `D4_RELATION`.
  - `T12_IFADAH_AUDIT` does not open `D5_IFADAH`.
  - `T13_HUKM_AUDIT` does not open `D6_HUKM`.
- Euclidean learning cannot produce rank above `CANDIDATE` for constitutional entities and cannot elevate execution authority to certified runtime control.
- Euclidean learning cannot write persistent runtime memory and cannot become `coverage_matrix_v0.1.yaml`.
- `predict_branch` returns audit suggestions, not system decisions.
- Failure learning records are learning artifacts and do not replace `FailureCode`.

## Constitutional Sequence
Domain → Contract → BridgeSpec → ProofObject → FailureAlignment → Kernel.
