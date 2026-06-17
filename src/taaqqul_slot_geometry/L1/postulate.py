"""
L1 Postulates — المسلّمات الخمس + المسلّمات التشغيلية الاثنتا عشرة.

Origin: docs/00_MAQOOL_CONSTITUTION.md §8 (Postulates)
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-11

Architecture:
    The five structural postulates (P1-P5) are self-evident truths governing L0.
    The twelve operational axioms (OA1-OA12) are the enabling conditions for
    the reasonableness verification algebra.

    === Structural Postulates (P1-P5) ===

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

    === Operational Axioms (OA1-OA12) ===

    OA1 — Origin Precedes Branch (الأصل سابق على الفرع)
    OA2 — No Weight Without Origin (لا وزن مرخّص بلا أصل مرخّص)
    OA3 — No Origin Without Prior Knowledge (لا أصل مرخّص بلا معرفة قبلية مصنّفة)
    OA4 — No Branch Without Shared Illah (لا فرع من أصل بلا علّة جامعة)
    OA5 — No Illah Without Attribute (لا علّة مؤثّرة بلا وصف مؤثّر)
    OA6 — Preventer Blocks Transition (لا انتقال مع وجود مانع)
    OA7 — Invalidating Difference (الفرق القادح يمنع القياس أو يخفض الرتبة)
    OA8 — Visible Residuals (كل نقص يُسجّل بقايا ولا يخفى)
    OA9 — Morphology Does Not Produce Hukm (الصرف لا ينتج حكمًا)
    OA10 — Syntax Does Not Produce Reality (النحو لا ينتج واقعًا)
    OA11 — Ifadah Requires Evidence (الإفادة لا تصبح حكمًا إلّا بدليل)
    OA12 — Evidence Requires Tahqiq (الدليل لا ينزل على الواقع إلّا بتحقيق مناط)

Every postulate/axiom carries:
    - postulate_id: unique identifier (e.g. "P1", "OA1")
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
    - OPERATIONAL: operational axioms for the reasoning algebra (OA1-OA12)
    """

    GROUNDING = "grounding"
    STRUCTURAL = "structural"
    PRESERVATION = "preservation"
    CONSTRAINT = "constraint"
    OPERATIONAL = "operational"


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
# §4  THE TWELVE OPERATIONAL AXIOMS (المسلّمات التشغيلية)
# ══════════════════════════════════════════════════════════════════════════════


AXIOM_OA1 = Postulate(
    postulate_id="OA1",
    name="Origin Precedes Branch",
    name_ar="الأصل سابق على الفرع",
    statement=(
        "No branch may exist without a prior licensed origin. "
        "The origin is ontologically and operationally prior to the branch."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1",
    related_failure_codes=(
        FailureCode.M_02_02.value,
    ),
)

AXIOM_OA2 = Postulate(
    postulate_id="OA2",
    name="No Weight Without Origin",
    name_ar="لا وزن مرخّص بلا أصل مرخّص",
    statement=(
        "No weight pattern is licensed unless there exists a licensed origin "
        "and a licensed branch that the weight witnesses."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P4; docs/55 §Origin",
    related_failure_codes=(
        FailureCode.M_02_19.value,
        FailureCode.M_00_22.value,
    ),
)

AXIOM_OA3 = Postulate(
    postulate_id="OA3",
    name="No Origin Without Prior Knowledge",
    name_ar="لا أصل مرخّص بلا معرفة قبلية مصنّفة",
    statement=(
        "No origin is licensed without prior classified knowledge. "
        "The prior knowledge is the enabling condition (shart imkan), "
        "not a final judgment or absolute truth."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md §Origins",
    related_failure_codes=(
        FailureCode.M_02_02.value,
    ),
)

AXIOM_OA4 = Postulate(
    postulate_id="OA4",
    name="No Branch Without Shared Illah",
    name_ar="لا فرع من أصل بلا علّة جامعة",
    statement=(
        "No branch may be derived from an origin without a shared illah "
        "(common cause) that binds origin and branch."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8",
    related_failure_codes=(
        FailureCode.M_02_04.value,
    ),
)

AXIOM_OA5 = Postulate(
    postulate_id="OA5",
    name="No Illah Without Effective Attribute",
    name_ar="لا علّة مؤثّرة بلا وصف مؤثّر",
    statement=(
        "No shared illah operates without an effective attribute "
        "(wasf mu'aththir) that makes it operative in the branch."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8",
    related_failure_codes=(
        FailureCode.M_02_04.value,
    ),
)

AXIOM_OA6 = Postulate(
    postulate_id="OA6",
    name="Preventer Blocks Transition",
    name_ar="لا انتقال مع وجود مانع",
    statement=(
        "No transition is licensed when an active preventer (mani') exists. "
        "The preventer blocks the transition regardless of other conditions."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8",
    related_failure_codes=(
        FailureCode.M_02_05.value,
    ),
)

AXIOM_OA7 = Postulate(
    postulate_id="OA7",
    name="Invalidating Difference",
    name_ar="الفرق القادح يمنع القياس أو يخفض الرتبة",
    statement=(
        "An invalidating difference (farq qadih) between origin and branch "
        "either blocks the qiyas entirely or lowers the rank of the result."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8",
    related_failure_codes=(
        FailureCode.M_02_05.value,
        FailureCode.M_CX_09.value,
    ),
)

AXIOM_OA8 = Postulate(
    postulate_id="OA8",
    name="Visible Residuals",
    name_ar="كل نقص يُسجّل بقايا ولا يخفى",
    statement=(
        "Every deficiency is recorded as a visible residual. "
        "No gap may be hidden or silently ignored. "
        "Residuals make incompleteness traceable, not fatal."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5",
    related_failure_codes=(
        FailureCode.M_CX_08.value,
    ),
)

AXIOM_OA9 = Postulate(
    postulate_id="OA9",
    name="Morphology Does Not Produce Hukm",
    name_ar="الصرف لا ينتج حكمًا",
    statement=(
        "Morphological analysis (sarf) does not produce a judgment (hukm). "
        "It produces licensed candidates and structural descriptions only."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P4; §6 L0",
    related_failure_codes=(
        FailureCode.M_03_09.value,
        FailureCode.M_02_19.value,
    ),
)

AXIOM_OA10 = Postulate(
    postulate_id="OA10",
    name="Syntax Does Not Produce Reality",
    name_ar="النحو لا ينتج واقعًا",
    statement=(
        "Syntactic relations (nahw) do not produce claims about external reality. "
        "They produce licensed relational structures only."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §6 L2",
    related_failure_codes=(
        FailureCode.M_03_11.value,
    ),
)

AXIOM_OA11 = Postulate(
    postulate_id="OA11",
    name="Ifadah Requires Evidence",
    name_ar="الإفادة لا تصبح حكمًا إلّا بدليل",
    statement=(
        "A linguistic utterance (ifadah) does not become a judgment (hukm) "
        "unless supported by external evidence. "
        "No claim may skip from expression to verdict without proof."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §6 L3",
    related_failure_codes=(
        FailureCode.M_03_04.value,
    ),
)

AXIOM_OA12 = Postulate(
    postulate_id="OA12",
    name="Evidence Requires Tahqiq al-Manat",
    name_ar="الدليل لا ينزل على الواقع إلّا بتحقيق مناط",
    statement=(
        "Evidence (dalil) does not apply to external reality unless "
        "tahqiq al-manat (verification of the operative cause in the particular case) "
        "is established. No general proof applies without particular verification."
    ),
    category=PostulateCategory.OPERATIONAL,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §6 L3",
    related_failure_codes=(
        FailureCode.M_03_03.value,
        FailureCode.M_03_19.value,
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# §5  REGISTRY (سِجل المسلّمات)
# ══════════════════════════════════════════════════════════════════════════════


POSTULATES: Tuple[Postulate, ...] = (
    POSTULATE_P1,
    POSTULATE_P2,
    POSTULATE_P3,
    POSTULATE_P4,
    POSTULATE_P5,
)
"""All 5 structural postulates in canonical order."""

OPERATIONAL_AXIOMS: Tuple[Postulate, ...] = (
    AXIOM_OA1,
    AXIOM_OA2,
    AXIOM_OA3,
    AXIOM_OA4,
    AXIOM_OA5,
    AXIOM_OA6,
    AXIOM_OA7,
    AXIOM_OA8,
    AXIOM_OA9,
    AXIOM_OA10,
    AXIOM_OA11,
    AXIOM_OA12,
)
"""All 12 operational axioms in canonical order."""

ALL_POSTULATES_AND_AXIOMS: Tuple[Postulate, ...] = POSTULATES + OPERATIONAL_AXIOMS
"""Combined registry: 5 structural + 12 operational = 17 total."""

POSTULATE_BY_ID: Dict[str, Postulate] = {
    p.postulate_id: p for p in ALL_POSTULATES_AND_AXIOMS
}
"""Lookup any postulate or axiom by ID."""


# ══════════════════════════════════════════════════════════════════════════════
# §6  PURE FUNCTIONS (دوال نقية)
# ══════════════════════════════════════════════════════════════════════════════


def get_postulate(postulate_id: str) -> Postulate:
    """Look up a postulate or axiom by its ID.

    Parameters
    ----------
    postulate_id : str
        The ID to look up (e.g. "P1", "OA1").

    Returns
    -------
    Postulate
        The matching postulate or axiom.

    Raises
    ------
    ValueError
        If the postulate_id is not found (M_01_09).
    """
    if postulate_id not in POSTULATE_BY_ID:
        raise ValueError(FailureCode.M_01_09.value)
    return POSTULATE_BY_ID[postulate_id]


def postulates_by_category(category: PostulateCategory) -> Tuple[Postulate, ...]:
    """Return all postulates/axioms belonging to a category.

    Parameters
    ----------
    category : PostulateCategory
        The category to filter by.

    Returns
    -------
    Tuple[Postulate, ...]
        All postulates/axioms in that category.
    """
    return tuple(p for p in ALL_POSTULATES_AND_AXIOMS if p.category == category)


def total_postulate_count() -> int:
    """Return the total number of structural postulates (always 5).

    Returns
    -------
    int
        The count of structural postulates in the registry.
    """
    return len(POSTULATES)


def total_axiom_count() -> int:
    """Return the total number of operational axioms (always 12).

    Returns
    -------
    int
        The count of operational axioms in the registry.
    """
    return len(OPERATIONAL_AXIOMS)


def total_combined_count() -> int:
    """Return the total count of all postulates and axioms (always 17).

    Returns
    -------
    int
        5 structural + 12 operational = 17.
    """
    return len(ALL_POSTULATES_AND_AXIOMS)


def verify_postulate_coverage() -> bool:
    """Verify that all 5 categories have at least one postulate or axiom.

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
