# Maqool Constitution — `docs/00_MAQOOL_CONSTITUTION.md`

## Preamble

This document is the root constitutional authority for the `Taaqol-GPT` system.
Every entity, operation, and transition in the codebase derives its legitimacy from this document.
Violations of the rules below constitute a **constitutional breach** and must be rejected with a named `FailureCode`.

---

## §1. Governance

- All implementation MUST reference this document via `trace_ref`.
- No code may be promoted to a higher layer until the lower layer is fully closed (§5).
- Green CI is NOT constitutional approval.

---

## §2. Four Priority Categories (38 Core Terms)

### Category 1 — Software Entities (14 terms)
`SlotGraph`, `Center`, `Slots`, `Edges`, `Boundaries`, `Operations`, `Rank`, `Residuals`, `Trace`,
`Gamma`, `Candidate`, `Verdict`, `TransitionGate`, `FailureCode`

### Category 2 — Detailed Linguistic Entities (12 terms)
`Phoneme`, `Grapheme`, `Vowel`, `PhoneticPattern` (8 patterns), `Syllable` (4 types),
`Utterance`, `Signifier`, `LinguisticSignified`, `ConventionalSignified`, `Union`, `Signification`, `Intelligible`

### Category 3 — Ontological Patterns (10 terms)
`Entity`, `Attribute`, `Event`, `State`, `Relation`, `Cause`, `Condition`, `Preventer`, `Time`, `Place`

### Category 4 — Meta-Language Levels (7 terms)
`L0` (Object Language), `L1` (Formal Description), `L2` (Semantic/Logical), `L3` (Real-world),
`LicensedBridge`, `Crossing`, `MetaClosure`

---

## §3. The Eight Phonetic Patterns (L0 — closed set)

| ID | Pattern | Description         |
|----|---------|---------------------|
| 1  | Ca      | Consonant + fatha   |
| 2  | Cu      | Consonant + damma   |
| 3  | Ci      | Consonant + kasra   |
| 4  | C∅      | Consonant + sukun   |
| 5  | Caa     | Consonant + alif madd |
| 6  | Cuu     | Consonant + waw madd  |
| 7  | Cii     | Consonant + ya madd   |
| 8  | CVC∅    | Consonant + vowel + consonant + sukun |

No 9th pattern may exist (MCE-1).

---

## §4. The Four Syllable Types (L0 — closed set)

| ID | Type | Pattern       |
|----|------|---------------|
| 1  | CV   | C + short V   |
| 2  | CVC  | C + V + C     |
| 3  | CVV  | C + long V    |
| 4  | CVCC | C + V + C + C |

No 5th syllable type may exist (MCE-2).

---

## §5. Architecture Rules (STRICT)

### Rule 1 — Layered Implementation Order
L0 → L1 → L2 → L3. NO CODE for L1 until L0 is fully closed.
NO CODE for L2 until L1 is fully closed. NO CODE for L3 until L2 is fully closed.

### Rule 2 — Mandatory Entity Fields
Every entity MUST carry:
- `trace_ref: str` — string referencing this constitution (e.g. `"docs/00_MAQOOL_CONSTITUTION.md §3"`)
- `rank: Literal["CANDIDATE"]` — ceiling rank; may never be promoted in L0
- `residuals: FrozenSet[str]` — residual bundle (may be empty frozenset)

### Rule 3 — Frozen Dataclasses
ALL data structures MUST use `@dataclass(frozen=True)` with `__post_init__` birth guards.

### Rule 4 — Pure Functions
ALL operations MUST be pure functions (no I/O, no side effects, no network calls).

### Rule 5 — Named Failures
Every rejection MUST return a `FailureCode` enum member, never a silent exception.

### Rule 6 — TransitionGate
Every transition between layers MUST pass through a `TransitionGate` that verifies identity preservation.

### Rule 7 — Identity Preservation Axiom
`Identity(source) ⊆ Identity(target)` for every transition. If identity is lost, raise `IdentityLossError`.

### Rule 8 — No Leap Axiom
`abs(idx_source - idx_target) == 1` for any transition. No skipping layers.

### Rule 9 — Meta-Language Bridge
No term may cross from L0→L1, L1→L2, or L2→L3 without a `LicensedBridge` with explicit `bridge_license_ref`.

### Rule 10 — No Meaning from Weight Alone
The weight layer (phonetic patterns) does NOT produce meaning. It only produces licensed candidates.

---

## §6. Layer Boundaries

### L0 (Object Language)
- All 28 Arabic graphemes
- All 8 phonetic patterns
- All 4 vowels + 3 madd
- All 4 syllable types
- Utterance sequences
- Jamid anchors (binary + ternary)
- Particles (harf al-maani)
- Weight patterns

### L1 (Formal Description)
- Formal definitions of all 38 terms
- Postulates for each category
- Common notions
- Licensed bridges from L0

### L2 (Semantic/Logical)
- Qiyas engine
- Proof engine
- Closure verification
- Licensed bridges from L1

### L3 (Real-world)
- Evidence types
- Manat verification
- Hukm candidates
- Tanzil (implementation)
- Licensed bridges from L2

---

## §7. Failure Codes (root taxonomy)

All 100 failure codes are enumerated in `src/taaqqul_slot_geometry/constitution/failure_taxonomy.py`.
The prefix convention is `M_<layer>_<number>`.

- `M_00_xx` — L0 violations
- `M_01_xx` — L1 violations
- `M_02_xx` — L2 violations
- `M_03_xx` — L3 violations
- `M_CX_xx` — Constitutional cross-cutting violations (identity, leap, bridge)

---

## §8. Postulates

### P1 — Sound Primacy
Every meaning must be mediated by a signifier. No signifier without phonological grounding.

### P2 — Closure
Every layer is closed under its own operations. No element of L(n) may be constructed from L(n+1).

### P3 — Identity Preservation
Every transition preserves the identity of the source. `Identity(source) ⊆ Identity(target)`.

### P4 — No Meaning from Weight
Phonetic weight does not produce meaning. Weight produces only licensed candidates.

### P5 — Exhaustiveness
The 8 phonetic patterns, 4 syllable types, and 28 graphemes are exhaustive and closed.

---

## §9. Common Notions

### CN1 — Self-Equality
Every entity is equal to itself.

### CN2 — Whole Greater Than Part
If A contains B and B is not empty, then A is greater than B.

### CN3 — Substitution
If A = B and B = C, then A = C.

### CN4 — Transitivity of Subsumption
If Identity(a) ⊆ Identity(b) and Identity(b) ⊆ Identity(c), then Identity(a) ⊆ Identity(c).

---

*End of Maqool Constitution v1.0*
