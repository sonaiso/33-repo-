# Failure Alignment Constitution — `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5`, `docs/08_PROOF_OBJECT_CONSTITUTION.md`, and `docs/09_COMPUTED_COVERAGE_CONSTITUTION.md`.

## Audit-Only Law (PR #38)
FailureAlignment is audit-only.
FailureAlignment does not replace FailureCode.
FailureAlignment does not open runtime.

## Alignment Constraints
- Every alignment row must define a primary canonical code.
- No executable row may use `NONE` as executable mapping.
- one-to-many alignment requires a primary canonical code.
- Alignment rows are review artifacts, not execution directives.

## Scope Boundary
This layer audits policy completeness and naming consistency only.
It does not authorize predicates, translators, decision engines, lexical lookup, or relation builders.
