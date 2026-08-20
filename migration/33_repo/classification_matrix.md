# 33-repo Classification Matrix (Audit-Only)

## Classification Labels

- `KEEP_AS_LAW`: preserve as a normative guardrail/law pattern.
- `RECONSTRUCT`: preserve function, but re-derive minimal primitive set in the new algebra-first repository.
- `COUNTERMODEL`: preserve as a historical overreach/error benchmark that must fail in the new core.
- `ARCHIVE`: preserve for history and vocabulary only; do not treat as primitive.

## Artifact-by-Artifact Matrix

| Artifact | Source | Class | Rationale |
|---|---|---|---|
| Runtime embargo constitutional constraints | `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md` | KEEP_AS_LAW | Safety boundary is still valid and transferable as governance law. |
| No meaning/role from weight alone constraints | `docs/00_MAQOOL_CONSTITUTION.md`, `docs/01_L0_PHONETIC_BOUNDARY.md`, `docs/11_LAFZI_FORM_CONSTITUTION.md` | KEEP_AS_LAW | Aligns with `NoRoleFromWeightAlone` and role-entitlement separation. |
| Identity preservation implementation | `src/taaqqul_slot_geometry/constitution/identity_preservation.py` | RECONSTRUCT | Useful function, but primitive status must be re-proven in minimal meta-core. |
| Transition gate implementation | `src/taaqqul_slot_geometry/constitution/transition_gate.py` | RECONSTRUCT | Useful sequencing constraint; should be rebuilt under deletion/reconstruction protocol. |
| Failure taxonomy breadth (~legacy enum scale) | `src/taaqqul_slot_geometry/constitution/failure_taxonomy.py` | ARCHIVE | Vocabulary source; full breadth is not a proven primitive set. |
| Legacy morphology theorem asserting `T(W)=transitivity_class` | `docs/19_MORPHOLOGY_GENERATOR_THEOREM.md` | COUNTERMODEL | Encodes a now-rejected authority leap from pattern to actual valency verdict. |
| Weight-layer runtime leap attempts | historical pattern represented by docs/tests guardrails | COUNTERMODEL | Must remain negative regression evidence in successor repository. |
| Euclidean presentation style | `docs/01_EUCLIDEAN_PROOFS.md` | RECONSTRUCT | Methodology remains useful, but axioms/theorems require re-ratification. |

## Migration Decision Rule

No artifact is directly transplanted into the new core by default.  
Default action is `RECONSTRUCT` unless the artifact is explicitly classified as `KEEP_AS_LAW` (governance-only) or `COUNTERMODEL` (negative regression), with `ARCHIVE` for historical-only preservation.

## Constitutional Invariants Preserved

- No runtime/domain opening is introduced.
- No forbidden files are introduced/modified.
- No rank promotion is introduced.
- No computed-verdict runtime behavior is introduced.

## Why This Is Audit-Only

This matrix is a governance artifact. It carries no execution semantics and does not change source/runtime behavior.
