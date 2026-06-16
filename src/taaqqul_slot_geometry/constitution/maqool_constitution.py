"""
MaqoolConstitution — root class encoding all postulates, definitions, and common notions.
Origin: docs/00_MAQOOL_CONSTITUTION.md
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class MaqoolConstitution:
    """Frozen singleton encoding the Maqool Constitution.

    All fields are frozen sets of string identifiers.  These sets are the
    authoritative references used by every entity's ``trace_ref``.

    Origin: docs/00_MAQOOL_CONSTITUTION.md
    """

    # 38 core terms (Categories 1–4)
    core_terms: FrozenSet[str] = field(
        default_factory=lambda: frozenset(
            {
                # Category 1 — Software Entities (14)
                "SlotGraph",
                "Center",
                "Slots",
                "Edges",
                "Boundaries",
                "Operations",
                "Rank",
                "Residuals",
                "Trace",
                "Gamma",
                "Candidate",
                "Verdict",
                "TransitionGate",
                "FailureCode",
                # Category 2 — Detailed Linguistic Entities (12)
                "Phoneme",
                "Grapheme",
                "Vowel",
                "PhoneticPattern",
                "Syllable",
                "Utterance",
                "Signifier",
                "LinguisticSignified",
                "ConventionalSignified",
                "Union",
                "Signification",
                "Intelligible",
                # Category 3 — Ontological Patterns (10)
                "Entity",
                "Attribute",
                "Event",
                "State",
                "Relation",
                "Cause",
                "Condition",
                "Preventer",
                "Time",
                "Place",
                # Category 4 — Meta-Language Levels (7)
                "L0",
                "L1",
                "L2",
                "L3",
                "LicensedBridge",
                "Crossing",
                "MetaClosure",
            }
        )
    )

    # Eight phonetic patterns (closed set — MCE-1)
    phonetic_patterns: FrozenSet[str] = field(
        default_factory=lambda: frozenset(
            {"Ca", "Cu", "Ci", "C∅", "Caa", "Cuu", "Cii", "CVC∅"}
        )
    )

    # Four syllable types (closed set — MCE-2)
    syllable_types: FrozenSet[str] = field(
        default_factory=lambda: frozenset({"CV", "CVC", "CVV", "CVCC"})
    )

    # Postulates (P1–P5)
    postulates: FrozenSet[str] = field(
        default_factory=lambda: frozenset(
            {
                "P1:sound_primacy",
                "P2:closure",
                "P3:identity_preservation",
                "P4:no_meaning_from_weight",
                "P5:exhaustiveness",
            }
        )
    )

    # Common notions (CN1–CN4)
    common_notions: FrozenSet[str] = field(
        default_factory=lambda: frozenset(
            {
                "CN1:self_equality",
                "CN2:whole_greater_than_part",
                "CN3:substitution",
                "CN4:transitivity_of_subsumption",
            }
        )
    )

    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        assert len(self.core_terms) == 43, (
            f"Expected 43 core terms, got {len(self.core_terms)}"
        )
        assert len(self.phonetic_patterns) == 8, (
            f"Expected 8 phonetic patterns, got {len(self.phonetic_patterns)}"
        )
        assert len(self.syllable_types) == 4, (
            f"Expected 4 syllable types, got {len(self.syllable_types)}"
        )


# Singleton instance — import this instead of instantiating directly.
CONSTITUTION = MaqoolConstitution()
