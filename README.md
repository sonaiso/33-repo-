# Taaqol-GPT — Slot Geometry Engine

A constitutionally-governed, layer-locked Arabic language analysis engine where every
entity is frozen, every function is pure, every rejection has a named `FailureCode`,
and no layer may be opened until the layer below it is fully closed.

## Governing Law

All implementation derives its legitimacy from:

```
docs/00_MAQOOL_CONSTITUTION.md
```

No code may be written without a `trace_ref` pointing to a section of this document.

## Architecture

The system is structured in four layers, opened strictly in order:

| Layer | Domain | Status |
|-------|--------|--------|
| L0 | Object Language (phonetics, graphemics, signification) | Complete |
| L1 | Formal Description (definitions, postulates, bridges) | Pending |
| L2 | Logical (qiyas, proof, closure) | Locked |
| L3 | Real-world (evidence, hukm, tanzil) | Locked |

## Package Layout

```
src/taaqqul_slot_geometry/
  constitution/   <- FailureCode, IdentityPreservation, TransitionGate, MaqoolConstitution
  core/           <- SlotGraph (9-tuple), Rank, ResidualBundle, TraceRef
  L0/             <- Phoneme, Grapheme, Vowel, Syllable, Utterance, Signifier,
                     Signified, Union, Signification, JamidAnchor, HarfMaani, Weight
  L1/             <- PENDING
  L2/             <- LOCKED
  L3/             <- LOCKED
```

## Mandatory Entity Fields

Every entity carries these constitutional fields (Rule 2):

| Field | Type | Constraint |
|-------|------|------------|
| `domain_tag` | `str` | Explicit meta-language domain marker |
| `trace_ref` | `str` | Non-empty reference to the constitution |
| `rank` | `str` | Always `"CANDIDATE"` in L0 |
| `residuals` | `FrozenSet[str]` | May be empty but must exist |

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

To run only L0 tests:

```bash
pytest tests/L0/ tests/constitution/
```

## Constitutional Guard

A CI-level guard enforces structural compliance:

```bash
python ci/constitutional_guard.py
```

This performs 150 checks across all entities and rejects any violation with a
named `FailureCode`.

## Key Constraints

- Frozen dataclasses with `__post_init__` birth guards (Rule 3)
- Pure functions only — no I/O, no network (Rule 4)
- Named failures — never silent exceptions (Rule 5)
- Identity preservation across transitions (Rule 7)
- No-Leap Axiom: layers advance one step at a time (Rule 8)
- No rank promotion beyond `CANDIDATE` in L0

## Documentation

See `docs/` for the full constitutional corpus:

- `00_MAQOOL_CONSTITUTION.md` — Root constitutional authority
- `01_L0_PHONETIC_BOUNDARY.md` — L0 boundary laws
- `02_L1_META_LANGUAGE_BOUNDARY.md` — L1 boundary laws
- `03_L2_LOGICAL_BOUNDARY.md` — L2 boundary laws
- `04_L3_REALITY_BOUNDARY.md` — L3 boundary laws
- `14_PR_CHAIN_ROADMAP.md` — Implementation roadmap
