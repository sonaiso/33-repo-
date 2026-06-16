# L0 Phonetic Boundary Laws — `docs/01_L0_PHONETIC_BOUNDARY.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §6` (L0 layer definition).

## Boundary Laws

### BL-L0-01 — No meaning from phonetic weight
A phonetic pattern (Ca, Cu, Ci, C∅, Caa, Cuu, Cii, CVC∅) does NOT produce meaning.
It produces only a licensed candidate with `rank = CANDIDATE`.

### BL-L0-02 — Closure of phonetic patterns
Exactly 8 phonetic patterns exist. No 9th pattern may be defined or instantiated.

### BL-L0-03 — Grapheme exhaustiveness
Exactly 28 Arabic graphemes exist, each with a defined articulation point and manner.

### BL-L0-04 — Syllable type closure
Exactly 4 syllable types exist (CV, CVC, CVV, CVCC). No 5th type may be defined.

### BL-L0-05 — Jamid anchor binary restriction
Binary jamid anchors (yd, dm, xd, fm) are NOT derivational roots.
Any attempt to derive from them MUST be rejected with `FailureCode.M_00_07`.

### BL-L0-06 — Vowel completeness
Exactly 4 short vowels (fatha, damma, kasra, sukun) and 3 madd vowels exist.

### BL-L0-07 — Sukun default for particles
Most particles (harf al-maani) are built on sukun (`is_built_on_sukun = True`).
This is a phonological fact, not a semantic one.

### BL-L0-08 — No rank promotion in L0
No entity in L0 may have its rank promoted beyond `CANDIDATE`.

### BL-L0-09 — Identity fields required
Every L0 entity MUST carry `trace_ref`, `rank`, and `residuals`.

### BL-L0-10 — Pure construction only
L0 entities are constructed by pure functions. No I/O, no side effects.
