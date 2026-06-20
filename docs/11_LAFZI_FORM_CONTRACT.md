# LAFZI_FORM Contract Constitution — `docs/11_LAFZI_FORM_CONTRACT.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5`, `docs/05_DOMAIN_REGISTRY_CONSTITUTION.md`, and `docs/07_GATE_BRIDGE_CONSTITUTION.md`.

## DomainID
- D2_LAFZI_FORM

## SharedOrigin
- `docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1` (layer order and no-leap governance)
- `docs/05_DOMAIN_REGISTRY_CONSTITUTION.md` (domain separation law)

## DomainOrigin
- `docs/05_DOMAIN_REGISTRY_CONSTITUTION.md ### D2_LAFZI_FORM`

## MRK requirements
- MRK proof must certify form-level processing only.
- MRK trace must preserve DAL carrier identity into form candidates.
- MRK proof must explicitly reject lexical/relation/hukm claims in this domain.

## Branch types
- RootFormCandidate
- PatternFormCandidate
- WordFormCandidate
- BareVerbFormCandidate
- JamidFormCandidate
- MasdarFormCandidate
- ToolFormCandidate
- MabniNounFormCandidate

## Layer contracts
- Source layer: DAL_ONLY outputs enter through an authorized bridge only.
- Active layer: LAFZI_FORM produces form candidates only.
- Exit layer: LEXICAL_MADLUL may open only through `LafziToLexicalBridge` with LexicalProof.

## Element contracts
- Carrier and haraka traces are inherited; no element may be detached from source identity.
- Every candidate must keep `trace_ref`, `rank`, and `residuals`.
- Every candidate rank remains `CANDIDATE`.

## Allowed operations
- root form extraction
- pattern form extraction
- word form classification
- bare verb form detection
- jamid/masdar/tool/mabni form labeling

## Forbidden outputs
- lexical meaning
- lexical usage
- relation
- ifadah
- hukm

## Required exit bridge
- `LafziToLexicalBridge`
- Executable lexical predicate + `LexicalProof` are mandatory before entering D3_LEXICAL_MADLUL.

## Failure codes
- `M_00_09` for unauthorized cross-domain jump.
- `M_00_10` for rank promotion beyond `CANDIDATE`.
- `M_00_11` for missing `trace_ref`.
- `M_00_22` for malformed contract payloads.

## Residual policy
- Blocking residual: missing bridge proof to lexical domain.
- Resolvable residual: unresolved pattern ambiguity with a declared resolver.
- Non-blocking residual: optional orthographic variants that do not alter form class.
- Trace residual: audit-only notes retained for downstream verification.
