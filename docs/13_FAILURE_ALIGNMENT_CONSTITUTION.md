# Failure Alignment Constitution — `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5`, `docs/08_PROOF_OBJECT_CONSTITUTION.md`, and `docs/09_COMPUTED_COVERAGE_CONSTITUTION.md`.

## Audit-Only Law (PR #38, PR #55)
FailureAlignment is audit-only.
FailureAlignment does not replace FailureCode.
FailureAlignment does not open runtime.

## Alignment Constraints
- Every alignment row must define a primary canonical code.
- Every alignment row must define `canonical_family` from the closed constitutional family set.
- Every alignment row must define `domain_scope`.
- Every alignment row must define `proof_obligation` (or `AUDIT_ONLY_LOCAL` while embargoed).
- Every alignment row must define `residual_policy`.
- Every alignment row must set `forbidden_runtime_use=true` while embargoed.
- Secondary canonical codes are optional supporting references and never replace the primary canonical code.
- No executable row may use `NONE` as executable mapping.
- Alignment rows are review artifacts, not execution directives.
- Under runtime embargo, all rows remain `is_executable_row=false` with `executable_mapping=AUDIT_ONLY`.

## Canonical Family Set (Closed Under Embargo)
- `TRACE`
- `RANK`
- `IDENTITY`
- `LAYER_LEAP`
- `MEANING_LEAK`
- `IFADAH_LEAK`
- `RELATION_PREREQUISITE`
- `HUKM_PREREQUISITE`
- `TANZIL_PREREQUISITE`
- `L0_SPECIFIC`
- `L1_SPECIFIC`
- `L2_SPECIFIC`
- `L3_SPECIFIC`
- `SCHEMA`
- `BRIDGE`
- `PURITY`
- `BRANCH_GOVERNANCE`
- `REFERENCE_ALGEBRA`
- `EVIDENCE`
- `MANAT`

## Scope Boundary
This layer audits policy completeness and naming consistency only.
It does not authorize predicates, translators, decision engines, lexical lookup, or relation builders.
