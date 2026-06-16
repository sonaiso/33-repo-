# Integration Specification — Runtime Constitutional Engine

**Origin:** docs/00_MAQOOL_CONSTITUTION.md (all sections)
**PR:** #2.5 — Activate Runtime Constitutional Engine
**Status:** ACTIVE

---

## 1. Overview

The Runtime Constitutional Engine transforms the Maqool Constitution from static
data structures into an **operational machine** that:

- Accepts Arabic phonological input (consonant + vowel)
- Produces a constitutionally-licensed `JamidUnit` output
- Maintains a full audit trace of every transformation step
- Rejects unconstitutional input with named `FailureCode` errors

---

## 2. Architecture

```
┌──────────────────────────────────────────────────────────┐
│                 ConstitutionalEngine                       │
├──────────────────────────────────────────────────────────┤
│  Step 1: consonant + vowel → PhonemeUnit    [§3 MCE-1]   │
│  Step 2: PhonemeUnit → Syllable             [§4 MCE-2]   │
│  Step 3: Syllable → Utterance               [§2 Cat.2]   │
│  Step 4: Utterance → Signifier              [§8 P1]      │
│  Step 5: Signifier + Weight → JamidUnit     [BL-L0-05]   │
├──────────────────────────────────────────────────────────┤
│  Output: JamidUnit(status=CANDIDATE) + TraceStep[5]      │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Pipeline Specification

### Step 1: Phoneme Construction

| Aspect | Detail |
|--------|--------|
| Input | `consonant: str`, `vowel: str` |
| Output | `PhonemeUnit` |
| Ref | §3 MCE-1 |
| Barrier | Empty consonant → `M_00_14`; invalid vowel → `M_00_02` |

### Step 2: Syllable Construction

| Aspect | Detail |
|--------|--------|
| Input | `PhonemeUnit` |
| Output | `Syllable` |
| Ref | §4 MCE-2 |
| Barrier | Invalid pattern for syllable → `M_00_03` |

### Step 3: Utterance Construction

| Aspect | Detail |
|--------|--------|
| Input | `Syllable` |
| Output | `Utterance` |
| Ref | §2 Category 2 |
| Barrier | Empty syllable sequence → `M_00_06` |

### Step 4: Signifier Construction

| Aspect | Detail |
|--------|--------|
| Input | `Utterance` |
| Output | `Signifier` |
| Ref | §8 P1 |
| Barrier | Missing utterance → `M_00_18` |

### Step 5: JamidUnit Construction

| Aspect | Detail |
|--------|--------|
| Input | `Signifier`, `PhonemeUnit`, `weight_pattern: str`, `root_letters: Tuple[str, ...]` |
| Output | `JamidUnit` |
| Ref | BL-L0-05 |
| Barrier | Invalid weight → `M_00_22`; empty root → `M_00_22` |

---

## 4. Constitutional Guarantees

| Guarantee | Mechanism | Verification |
|-----------|-----------|--------------|
| No Leap | Steps numbered 1-5 sequentially | `verify_no_leap(trace)` |
| Identity Preserved | Each step declares `identity_preserved=True` | `verify_identity_preserved(trace)` |
| Rank Ceiling | Output is always `CANDIDATE` | Birth guard in `JamidUnit.__post_init__` |
| Named Failures | All rejections use `ConstitutionalRuntimeError` | `failure_code` attribute on exception |
| Frozen Output | `@dataclass(frozen=True)` on all entities | Mutation raises `FrozenInstanceError` |
| Trace Ref | Every entity has `trace_ref` | Birth guard checks non-empty |

---

## 5. Input Specification

### Accepted Vowels (Arabic + English)

| Arabic | English | Pattern |
|--------|---------|---------|
| فتحة | fatha | `C_FATHA` (Ca) |
| ضمة | damma | `C_DAMMA` (Cu) |
| كسرة | kasra | `C_KASRA` (Ci) |
| سكون | sukun | `C_SUKUN` (C∅) |
| مد_ألف | alif_madd | `C_FATHA_MADD` (Caa) |
| مد_واو | waw_madd | `C_DAMMA_MADD` (Cuu) |
| مد_ياء | ya_madd | `C_KASRA_MADD` (Cii) |

**Note:** Sukun (`C_SUKUN`) alone cannot form a syllable. It must be part of a
CVC structure with another phoneme. This is constitutionally correct per MCE-2.

### Accepted Weight Patterns (Arabic + English)

| Arabic | English | Pattern |
|--------|---------|---------|
| جذر | root | `ROOT` |
| فَعَلَ | faala | `FAALA` |
| فَعْل | faal | `FAAL` |
| فِعَال | fiaal | `FIAAL` |
| فُعَال | fual | `FUAL` |
| فَاعِل | faalil | `FAALIL` |
| مَفْعُول | mafuul | `MAFUUL` |
| تَفَاعَلَ | tafaala | `TAFAALA` |
| اسْتَفْعَلَ | istafala | `ISTAFALA` |

---

## 6. Error Specification

All errors are raised as `ConstitutionalRuntimeError` with:
- `message`: Human-readable description
- `failure_code`: `FailureCode` enum member

| Failure Code | Trigger |
|-------------|---------|
| `M_00_14` | Empty consonant |
| `M_00_02` | Invalid vowel name |
| `M_00_03` | Pattern cannot form syllable |
| `M_00_06` | Empty syllable sequence |
| `M_00_18` | Missing utterance/signifier |
| `M_00_22` | Invalid weight or empty root |

---

## 7. Test Coverage

### E2E Tests (25 tests)

- 5 basic pipeline tests (fatha, damma, kasra, madd_alif, madd_waw)
- 5 Arabic input tests (فتحة, ضمة, كسرة, سكون/rejection, مد_ألف)
- 5 trace verification tests (5 steps, sequential, no-leap, identity, refs)
- 5 rejection tests (empty consonant, invalid vowel, invalid weight, empty root, step1 failure)
- 5 output structure tests (frozen, trace_ref, rank, signifier, phoneme)

### Property Tests (10 test classes)

1. Weight never produces meaning alone (9 weights)
2. No leap within pipeline (11 consonants)
3. Identity preserved for all vowels (6 vowels)
4. Rank never exceeds CANDIDATE (5 roots)
5. Trace ref always present (11 consonants)
6. Frozen immutability (6 vowels)
7. Named failures for invalid vowels (5 cases)
8. Pipeline consistency (6 consonant+vowel pairs)
9. All weight patterns accepted (9 weights)
10. Cross-validation with L0 entities (3 consonant+vowel pairs)

---

## 8. CI/CD Integration

The Constitutional Guard (`ci/constitutional_guard.py`) performs:

1. **Trace ref check** — every source file references the constitution
2. **Frozen dataclass check** — all `@dataclass` use `frozen=True`
3. **No I/O check** — source files (excluding CI/tests) have no I/O
4. **Rank ceiling check** — no rank promotion beyond CANDIDATE
5. **L3-in-L0 check** — no L3 constructs in L0 code

Usage:
```bash
python -m ci.constitutional_guard --pr-number 3 --branch feat/L1-morphology
```

---

## 9. Usage Example

```python
from taaqqul_slot_geometry.runtime.constitutional_engine import ConstitutionalEngine

engine = ConstitutionalEngine()

# Full pipeline
jamid, trace = engine.full_pipeline(
    consonant="ك", vowel="فتحة",
    weight_pattern="فَعَلَ",
    root_letters=("ك", "ت", "ب"),
)

# Verify constitutional compliance
assert jamid.status == "CANDIDATE"
assert ConstitutionalEngine.verify_no_leap(trace)
assert ConstitutionalEngine.verify_identity_preserved(trace)

# Individual steps
phoneme = engine.step1_phoneme("ب", "ضمة")
syllable = engine.step2_syllable(phoneme)
utterance = engine.step3_utterance(syllable)
signifier = engine.step4_signifier(utterance)
```

---

## 10. Layer Lock Status

| Layer | Status | Engine Support |
|-------|--------|---------------|
| L0 | ACTIVE | Full pipeline implemented |
| L1 | PENDING | Awaits L0 closure declaration |
| L2 | LOCKED | Requires L1 closure |
| L3 | LOCKED | Requires L2 closure |

---

*End of Integration Specification*
