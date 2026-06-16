# L3 Reality Boundary Laws — `docs/04_L3_REALITY_BOUNDARY.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §6` (L3 layer definition).

## Status
**PENDING** — L3 may not be implemented until L2 is fully closed (Rule 1).

## Boundary Laws (Reserved)

### BL-L3-01 — No L3 without L2 closure
Evidence and manat verification require L2 to be fully closed first.

### BL-L3-02 — Bridge requirement
Every L2→L3 crossing requires a `LicensedBridge` with `bridge_license_ref`.

### BL-L3-03 — Evidence types
Four evidence types are recognized: testimony, observation, tawatur, textual.

### BL-L3-04 — Manat requirement
Every hukm candidate requires manat verification before tanzil.

### BL-L3-05 — No HukmCandidate in L0 or L1
HukmCandidate and TanzilCandidate may only exist in L3. Any attempt to instantiate them
in L0/L1/L2 MUST be rejected with `FailureCode.M_CX_05`.
