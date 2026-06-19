# Domain Registry Constitution — `docs/05_DOMAIN_REGISTRY_CONSTITUTION.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5` and `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`.

## Domain Separation Law

No candidate without domain.
No domain without origin.
No origin without MRKProof.
No exit from domain without BridgeProof.

## Canonical L1 Domain IDs

- D0_TRACE
- D1_DAL_ONLY
- D2_LAFZI_MADLUL_ONLY
- D3_LEXICAL_MADLUL
- D4_RELATION
- D5_IFADAH
- D6_HUKM
- D7_TANZIL

## Required Contract Headers Per Domain

Each domain contract must define:
- DomainID
- SharedOrigin
- DomainOrigin
- MRK requirements
- Branch types
- Layer contracts
- Element contracts
- Allowed operations
- Forbidden outputs
- Required exit bridge
- Failure codes
- Residual policy

## Cross-Domain Restrictions

No direct DalOnly → LexicalMadlul.
No LafziMadlul → LexicalMadlul without LexicalProof.
No LexicalMadlul → Relation without RelationBridge.
