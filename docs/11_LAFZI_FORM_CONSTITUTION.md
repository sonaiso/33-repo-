# LAFZI_FORM Constitution — `docs/11_LAFZI_FORM_CONSTITUTION.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5`, `docs/05_DOMAIN_REGISTRY_CONSTITUTION.md`, and `docs/10_DAL_ATOMIC_CONSTITUTION.md`.

## DomainID
- D2_LAFZI_FORM

## Scope
LAFZI_FORM is a pure form layer. It accepts only authorized DAL_ONLY surface candidates and outputs form candidates only.

## Allowed outputs
- RootFormCandidate
- PatternFormCandidate
- WordFormCandidate
- BareTriliteralVerbFormCandidate
- BareQuadriliteralVerbFormCandidate
- TriliteralJamidFormCandidate
- QuadriliteralJamidFormCandidate
- MasdarFormCandidate
- ToolFormCandidate
- MabniNounFormCandidate

## Entry constraints
- `source_domain_id` must be `D1_DAL_ONLY`.
- `source_surface_ref` is mandatory.
- `required_bridge_ref` must be `DalToLafziBridgeSpec`.
- `proof_object_ref` or `proof_trace_ref` is mandatory.
- `rank` is locked to `CANDIDATE`.

## Forbidden outputs
- LEXICAL_MEANING
- LEXICAL_ROOT
- USAGE
- RELATION
- TOOL_MEANING
- MASDAR_MEANING
- TRANSITIVITY
- ISNAD
- IFADAH
- HUKM
- TANZIL

## Guard principles
- RootFormCandidate is not LexicalRoot.
- ToolFormCandidate is not ToolMeaning.
- MasdarFormCandidate is not MasdarMeaning.
- BareVerb form candidates do not carry transitivity or isnad.
- No runtime predicates, runtime translators, or kernel decisions in this phase.

## Layer sequencing
- DAL_ONLY → LAFZI_FORM is the only authorized opening at this stage.
- LAFZI_FORM → LEXICAL_MADLUL remains contract-gated and is not opened here.

## LAFZI-C2 Contract Refinement
- LAFZI-C2 refines form-only contracts and does not open lexical meaning.
- `arity` and `addition_status` are structural metadata only.
- `NO_ADDITION` means no form-level addition is claimed; it is not lexical purity.
- RootFormCandidate is not LexicalRoot.
- PatternFormCandidate is not semantic weight meaning.
- BareVerbFormCandidate is not tense/valency/isnad.
- MasdarFormCandidate is not MasdarMeaning.
- ToolFormCandidate is not ToolMeaning.
- MabniNounFormCandidate is not reference resolution or lexical usage.
- D2_LAFZI_FORM may only exit through a future `LafziToLexicalBridgeSpec`, not in this PR.

## Failure codes
- `M_00_09` for invalid cross-domain jump.
- `M_01_14` for missing L1 trace reference.
- `M_01_16` for rank promotion beyond CANDIDATE.
- `M_00_22` for malformed contract payloads.
