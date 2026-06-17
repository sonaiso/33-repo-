"""
L1 Postulates — المسلّمات الخمس.

Origin: docs/00_MAQOOL_CONSTITUTION.md §8 (Postulates)
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-11

Architecture:
    The five postulates (P1-P5) are self-evident truths that require no proof.
    They serve as axiomatic foundations for all reasoning in the system.

    P1 — Sound Primacy (أولوية الصوت):
        Every meaning must be mediated by a signifier.
        No signifier without phonological grounding.

    P2 — Closure (الإغلاق):
        Every layer is closed under its own operations.
        No element of L(n) may be constructed from L(n+1).

    P3 — Identity Preservation (ثبات الهوية):
        Every transition preserves the identity of the source.
        Identity(source) ⊆ Identity(target).

    P4 — No Meaning from Weight (لا معنى من الوزن):
        Phonetic weight does not produce meaning.
        Weight produces only licensed candidates.

    P5 — Exhaustiveness (الاستيعاب):
        The 8 phonetic patterns, 4 syllable types, and 28 graphemes
        are exhaustive and closed.

Every postulate carries:
    - postulate_id: unique identifier (e.g. "P1")
    - name: human-readable name
    - statement: formal statement of the postulate
    - trace_ref: constitutional reference
    - rank: always "CANDIDATE"
    - residuals: residual bundle (FrozenSet)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Dict, FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


# ══════════════════════════════════════════════════════════════════════════════
# §1  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════


@unique
class PostulateCategory(str, Enum):
    """Categories of postulates — فروع المسلّمات.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §8

    Each postulate belongs to a category describing what aspect of
    the system it governs:
    - GROUNDING: connects form to meaning (P1)
    - STRUCTURAL: governs layer architecture (P2, P5)
    - PRESERVATION: governs transitions (P3)
    - CONSTRAINT: limits what can be derived (P4)
    """

    GROUNDING = "grounding"
    STRUCTURAL = "structural"
    PRESERVATION = "preservation"
    CONSTRAINT = "constraint"


# ══════════════════════════════════════════════════════════════════════════════
# §2  POSTULATE ENTITY (المسلّمة)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class Postulate:
    """A formal postulate — مسلّمة.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §8

    A postulate is a self-evident truth that requires no proof (لا تُبرهَن).
    It serves as an axiomatic foundation from which theorems are derived.

    Parameters
    ----------
    postulate_id : str
        Unique identifier (e.g. "P1", "P2").
    name : str
        Human-readable name (e.g. "Sound Primacy").
    name_ar : str
        Arabic name (e.g. "أولوية الصوت").
    statement : str
        Formal statement of the postulate.
    category : PostulateCategory
        Which category this postulate governs.
    constitution_ref : str
        Reference to the constitution section.
    related_failure_codes : Tuple[str, ...]
        FailureCode values that this postulate guards against.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    postulate_id: str
    name: str
    name_ar: str
    statement: str
    category: PostulateCategory
    constitution_ref: str
    related_failure_codes: Tuple[str, ...] = ()
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §8"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Birth guard — validates all postulate fields."""
        if not self.postulate_id:
            raise ValueError(FailureCode.M_01_09.value)
        if not self.name:
            raise ValueError(FailureCode.M_01_09.value)
        if not self.name_ar:
            raise ValueError(FailureCode.M_01_09.value)
        if not self.statement:
            raise ValueError(FailureCode.M_01_09.value)
        if not isinstance(self.category, PostulateCategory):
            raise ValueError(FailureCode.M_01_19.value)
        if not self.constitution_ref:
            raise ValueError(FailureCode.M_01_03.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)


# ══════════════════════════════════════════════════════════════════════════════
# §3  THE FIVE POSTULATES (المسلّمات الخمس)
# ══════════════════════════════════════════════════════════════════════════════


POSTULATE_P1 = Postulate(
    postulate_id="P1",
    name="Sound Primacy",
    name_ar="أولوية الصوت",
    statement=(
        "Every meaning must be mediated by a signifier. "
        "No signifier without phonological grounding."
    ),
    category=PostulateCategory.GROUNDING,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P1",
    related_failure_codes=(
        FailureCode.M_00_01.value,
        FailureCode.M_00_18.value,
    ),
)

POSTULATE_P2 = Postulate(
    postulate_id="P2",
    name="Closure",
    name_ar="الإغلاق",
    statement=(
        "Every layer is closed under its own operations. "
        "No element of L(n) may be constructed from L(n+1)."
    ),
    category=PostulateCategory.STRUCTURAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P2",
    related_failure_codes=(
        FailureCode.M_CX_02.value,
        FailureCode.M_CX_05.value,
    ),
)

POSTULATE_P3 = Postulate(
    postulate_id="P3",
    name="Identity Preservation",
    name_ar="ثبات الهوية",
    statement=(
        "Every transition preserves the identity of the source. "
        "Identity(source) ⊆ Identity(target)."
    ),
    category=PostulateCategory.PRESERVATION,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P3",
    related_failure_codes=(
        FailureCode.M_CX_01.value,
    ),
)

POSTULATE_P4 = Postulate(
    postulate_id="P4",
    name="No Meaning from Weight",
    name_ar="لا معنى من الوزن",
    statement=(
        "Phonetic weight does not produce meaning. "
        "Weight produces only licensed candidates."
    ),
    category=PostulateCategory.CONSTRAINT,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P4",
    related_failure_codes=(
        FailureCode.M_02_19.value,
    ),
)

POSTULATE_P5 = Postulate(
    postulate_id="P5",
    name="Exhaustiveness",
    name_ar="الاستيعاب",
    statement=(
        "The 8 phonetic patterns, 4 syllable types, and 28 graphemes "
        "are exhaustive and closed."
    ),
    category=PostulateCategory.STRUCTURAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P5",
    related_failure_codes=(
        FailureCode.M_00_02.value,
        FailureCode.M_00_03.value,
        FailureCode.M_00_05.value,
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# §4  REGISTRY (سِجل المسلّمات)
# ══════════════════════════════════════════════════════════════════════════════


POSTULATES: Tuple[Postulate, ...] = (
    POSTULATE_P1,
    POSTULATE_P2,
    POSTULATE_P3,
    POSTULATE_P4,
    POSTULATE_P5,
)
"""All 5 postulates in canonical order."""

POSTULATE_BY_ID: Dict[str, Postulate] = {p.postulate_id: p for p in POSTULATES}
"""Lookup postulate by ID."""


# ══════════════════════════════════════════════════════════════════════════════
# §5  PURE FUNCTIONS (دوال نقية)
# ══════════════════════════════════════════════════════════════════════════════


def get_postulate(postulate_id: str) -> Postulate:
    """Look up a postulate by its ID.

    Parameters
    ----------
    postulate_id : str
        The ID to look up (e.g. "P1").

    Returns
    -------
    Postulate
        The matching postulate.

    Raises
    ------
    ValueError
        If the postulate_id is not found (M_01_09).
    """
    if postulate_id not in POSTULATE_BY_ID:
        raise ValueError(FailureCode.M_01_09.value)
    return POSTULATE_BY_ID[postulate_id]


def postulates_by_category(category: PostulateCategory) -> Tuple[Postulate, ...]:
    """Return all postulates belonging to a category.

    Parameters
    ----------
    category : PostulateCategory
        The category to filter by.

    Returns
    -------
    Tuple[Postulate, ...]
        All postulates in that category.
    """
    return tuple(p for p in POSTULATES if p.category == category)


def total_postulate_count() -> int:
    """Return the total number of postulates (always 5).

    Returns
    -------
    int
        The count of postulates in the registry.
    """
    return len(POSTULATES)


def verify_postulate_coverage() -> bool:
    """Verify that all 4 categories have at least one postulate.

    Returns
    -------
    bool
        True if all categories are covered.

    Raises
    ------
    ValueError
        If any category has no postulates (M_01_19).
    """
    for category in PostulateCategory:
        if not postulates_by_category(category):
            raise ValueError(FailureCode.M_01_19.value)
    return True
