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

## Strategic Vision

> **"لا كود بلا أصل، ولا فرع بلا ترخيص، ولا انتقال بلا إثبات"**

The project builds an Arabic language analysis engine across 4 sequential layers.
See `docs/16_STRATEGIC_METHODOLOGY.md` for the full strategic methodology with
measurable KPIs enforced through `pytest tests/test_kpi_indicators.py`.

---

## Binding Rules for All Agents

**Every agent (human or AI) working on this codebase MUST:**

1. **Trace every change** to the roadmap (`docs/15_PROJECT_ROADMAP.md`) or constitution
2. **Obtain a BranchLicense** for any work not explicitly listed in the roadmap
3. **Never write code** without a `trace_ref` to the constitution
4. **Never open a locked layer** — L1 is pending L0 closure, L2/L3 are locked
5. **Never introduce silent exceptions** — all rejections use `FailureCode`
6. **Never mutate entities** — all dataclasses must be `frozen=True`
7. **Never perform I/O** in source code — pure functions only
8. **Run KPI tests** before submitting: `pytest tests/test_kpi_indicators.py`
9. **Run the CI guard**: `python -m ci.constitutional_guard --source-dir src`
10. **Follow the branching governance** — see `docs/15_PROJECT_ROADMAP.md §حوكمة التفريع`

---

## Layer Order (immutable)

```
L0 (Object Language)  →  L1 (Formal Description)  →  L2 (Logical)  →  L3 (Real-world)
```

**Current phase: L0 Complete, awaiting formal closure (PR-9)**

See `docs/15_PROJECT_ROADMAP.md` for the full roadmap.

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

## Branching Governance (M_CX_16..M_CX_20)

No work is permitted outside the roadmap without a `BranchLicense`:

| Condition | Description | Failure Code |
|-----------|-------------|--------------|
| `roadmap_ref` | Must reference a numbered PR or roadmap section | `M_CX_16` |
| `trunk_complete` | Parent trunk must be minimally complete | `M_CX_17` |
| `motive` | Why this branch exists (دافع) | `M_CX_18` |
| `qualifying_difference` | Essential distinction from trunk (فرق قادح) | `M_CX_19` |
| `barrier_absent` | Verify no blocking barrier exists (مانع) | `M_CX_20` |

Usage:
```python
from taaqqul_slot_geometry.constitution import BranchLicense

license = BranchLicense(
    roadmap_ref="docs/15_PROJECT_ROADMAP.md Phase 1 PR-10",
    parent_ref="Phase 0 — L0 Closure",
    trunk_complete=True,
    motive="Convert L0 entities to formal definitions",
    description="L1/definition.py — formal definition for each L0 entity",
    qualifying_difference="L0 = raw entities, L1 = formal definitions with boundary conditions",
    condition="L0 formally closed",
    cause="Logical reasoning needs formal definitions as input",
    barrier_absent=True,
    barrier_check_description="No L0 entity incomplete or residual open",
)
```

---

## Package Structure

```
src/taaqqul_slot_geometry/
  constitution/   ← FailureCode, IdentityPreservation, TransitionGate,
                    MaqoolConstitution, BranchLicense
  core/           ← SlotGraph (9-tuple), Rank, ResidualBundle, TraceRef
  L0/             ← Phoneme, Grapheme, Vowel, Syllable, Utterance, Signifier,
                     Signified, Union, Signification, JamidAnchor, HarfMaani,
                     Weight, WaqfWasl
  L1/             ← PENDING (requires PR-9: L0 formal closure)
  L2/             ← LOCKED
  L3/             ← LOCKED
  runtime/        ← ConstitutionalEngine (5-step pipeline)
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

To run KPI indicators:

```bash
pytest tests/test_kpi_indicators.py -v
```

To run the CI constitutional guard:

```bash
python -m ci.constitutional_guard --source-dir src
```

---

## KPI Tests (docs/16_STRATEGIC_METHODOLOGY.md §7)

Every PR must pass these measurable indicators:

| KPI | Description | Target |
|-----|-------------|--------|
| KPI-01 | trace_ref coverage | 100% |
| KPI-02 | frozen compliance | 100% |
| KPI-03 | FailureCode coverage | 100% |
| KPI-04 | L0 entity count | 13 |
| KPI-05 | No layer leak | 0 |
| KPI-06 | CI guard clean | 0 violations |
| KPI-07 | No open residuals | 0 |

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

## Documentation Map

| Document | Purpose |
|----------|---------|
| `docs/00_MAQOOL_CONSTITUTION.md` | Root constitutional authority |
| `docs/01_L0_PHONETIC_BOUNDARY.md` | L0 boundary laws (10 laws) |
| `docs/01_EUCLIDEAN_PROOFS.md` | 4 foundational theorems |
| `docs/14_PR_CHAIN_ROADMAP.md` | Numbered PR chain |
| `docs/15_PROJECT_ROADMAP.md` | Full roadmap + branching governance |
| `docs/16_STRATEGIC_METHODOLOGY.md` | Strategic goals + KPIs |
| `docs/19_MORPHOLOGY_GENERATOR_THEOREM.md` | Generative morphology (TH7-TH9) |
| `docs/20_WAQF_WASL_BOUNDARY_THEOREM.md` | Stopping/joining laws (TH6.5) |

---

## Best Practices for Agents

1. **Read the roadmap first** — `docs/15_PROJECT_ROADMAP.md` defines what's allowed
2. **Check current phase** — only L0 work is permitted until PR-9 closes L0
3. **Run KPIs before commit** — `pytest tests/test_kpi_indicators.py`
4. **Run CI guard** — `python -m ci.constitutional_guard --source-dir src`
5. **Use `BranchLicense`** for any work not in the roadmap
6. **Follow the No-Leap Axiom** — work proceeds one layer at a time
7. **Never skip birth guards** — every `@dataclass(frozen=True)` has `__post_init__`
8. **Document the authority** — every file needs `Origin:` or `trace_ref`
9. **Keep functions pure** — no side effects, no I/O, no network
10. **Name every rejection** — use `FailureCode.M_XX_YY`, never bare exceptions

---

*End of CLAUDE.md*
