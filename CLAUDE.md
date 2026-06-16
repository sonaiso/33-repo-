# CLAUDE.md — Load-bearing Constitutional References

## Root Authority

All implementation in this repository derives its legitimacy from:

```
docs/00_MAQOOL_CONSTITUTION.md
```

This document is the Maqool Constitution for the `Taaqol-GPT` system.
**No code may be written without a `trace_ref` pointing to a section of this document.**

---

## Architecture in One Sentence

> A constitutionally-governed, layer-locked Arabic language analysis engine where every
> entity is frozen, every function is pure, every rejection has a named `FailureCode`,
> and no layer may be opened until the layer below it is fully closed.

---

## Layer Order (immutable)

```
L0 (Object Language)  →  L1 (Formal Description)  →  L2 (Logical)  →  L3 (Real-world)
```

**Current phase: L0**  — see `docs/14_PR_CHAIN_ROADMAP.md`.

---

## Mandatory Entity Fields (Rule 2)

Every entity in this codebase MUST carry:

| Field | Type | Constraint |
|-------|------|------------|
| `trace_ref` | `str` | Non-empty reference to the constitution |
| `rank` | `str` | Always `"CANDIDATE"` — never promoted in L0 |
| `residuals` | `FrozenSet[str]` | May be empty but must exist |

---

## Five Constitutional Rules (frequently referenced)

| Rule | Summary | Failure Code |
|------|---------|--------------|
| Rule 3 | Frozen dataclasses with `__post_init__` birth guards | `M_CX_06` |
| Rule 4 | Pure functions — no I/O, no network | `M_CX_07` |
| Rule 5 | Named failures — never silent exceptions | `M_CX_08` |
| Rule 7 | Identity preservation: `Identity(src) ⊆ Identity(tgt)` | `M_CX_01` |
| Rule 8 | No-Leap Axiom: `abs(src_idx - tgt_idx) == 1` | `M_CX_02` |

---

## Package Structure

```
src/taaqqul_slot_geometry/
  constitution/   ← FailureCode, IdentityPreservation, TransitionGate, MaqoolConstitution
  core/           ← SlotGraph (9-tuple), Rank, ResidualBundle, TraceRef
  L0/             ← Phoneme, Grapheme, Vowel, Syllable, Utterance, Signifier,
                     Signified, Union, Signification, JamidAnchor, HarfMaani, Weight
  L1/             ← PENDING
  L2/             ← LOCKED
  L3/             ← LOCKED
```

---

## How to Run Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

To run only L0 tests:

```bash
pytest tests/L0/ tests/constitution/
```

---

## Closed Sets (must never be extended without constitutional amendment)

| Set | Count | Ref |
|-----|-------|-----|
| Phonetic patterns | 8 | Constitution §3 (MCE-1) |
| Syllable types | 4 | Constitution §4 (MCE-2) |
| Arabic graphemes | 28 | Constitution §2 Category 2 |
| Short vowels | 4 | Constitution §2 Category 2 |
| Madd vowels | 3 | Constitution §2 Category 2 |
| Binary jamid anchors | 4 | Boundary law BL-L0-05 |
| Ternary jamid anchors | 3 | Boundary law BL-L0-05 |

---

## What is Forbidden in L0

- `HukmCandidate` — L3 only (`M_03_09`)
- `TanzilCandidate` — L3 only (`M_03_10`)
- `RealityClaim` — L3 only (`M_03_11`)
- `MajazVerdict` — L3 only (`M_03_12`)
- `NaqlVerdict` — L3 only (`M_03_13`)
- Any I/O, network, or filesystem access (`M_CX_10`, `M_CX_11`, `M_CX_15`)
- Rank promotion beyond `CANDIDATE` (`M_CX_09`)
- Treating binary jamid as derivational root (`M_00_07`)
- Deriving meaning from phonetic weight alone (`M_02_19`)

---

*End of CLAUDE.md*
