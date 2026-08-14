# Migration Acceptance Criteria (Audit-Only)

## Purpose

Define mandatory acceptance gates for any migration decision from `33-repo-` to an algebra-first successor repository, with explicit regression obligations.

## Repository Posture Gate

- `33-repo-` is treated as `Legacy Euclidean Arabic Prototype`.
- This repository is reference/corpus oriented for migration, not the new-core implementation baseline.

## Mandatory Gates

1. **Constitutional Gate**
- The migration record cites constitutional authority docs and restates runtime embargo + locked-layer bounds.

2. **Minimality Gate**
- The candidate artifact is proven necessary under deletion/reconstruction logic.
- If deletion preserves required behavior, artifact is not admitted as primitive.

3. **Classification Gate**
- Every artifact has one explicit class: `KEEP_AS_LAW`, `RECONSTRUCT`, `COUNTERMODEL`, or `ARCHIVE`.
- Justification is written and test-linked.

4. **Non-Transplant Gate**
- No direct source copy into new meta-core by default.
- Any direct copy requires explicit exception plus constitutional rationale.

5. **Regression Gate (Mandatory)**
- The successor repo must include an explicit regression benchmark:
  - `Weight ≠ ActualValencyVerdict`
  - `Weight` may produce only a capability/hypothesis candidate, not final relational-role entitlement.
- Any old claim equivalent to `T(W)=transitivity_class` is expected to fail entitlement without extra support structure.

6. **Security and Embargo Gate**
- No runtime authority, kernel opening, or decision-engine authority is introduced through migration artifacts.
- No secret-bearing data is introduced.

## Required Migration Deliverables Per Artifact

- Artifact identity (`source path`, `target intention`)
- Chosen class and rationale
- Positive and negative regression cases
- Residual risk statement
- Final verdict: `ACCEPTED`, `RECONSTRUCT_REQUIRED`, `COUNTERMODEL_ONLY`, or `ARCHIVED`

## Acceptance Exit Condition

Migration planning is accepted only when all artifacts in scope have:

- explicit classification,
- benchmark linkage,
- and constitutional-boundary compliance.

## Why This Is Audit-Only

This document defines governance and test obligations only. It introduces no executable behavior and no runtime admission.
