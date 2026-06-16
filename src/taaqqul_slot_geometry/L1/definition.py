"""
L1 Formal Definitions — التعريفات الرسمية (أصول وفروع).

Origin: docs/00_MAQOOL_CONSTITUTION.md §6 L1 (Formal Description)
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-10

Architecture (أصول وفروع — Roots and Branches):
    الأصل (FormalDefinition) ─── the root: every definition derives from this base
        │
        ├── فرع التصنيف (DefinitionCategory) ─── branches by category
        │       ├── PHONOLOGICAL  ─── phonemes, graphemes, vowels, syllables
        │       ├── COMPOSITIONAL ─── utterance, signifier, signified, union
        │       ├── SEMANTIC      ─── signification, jamid, harf_maani
        │       └── STRUCTURAL    ─── weight, waqf_wasl
        │
        ├── فرع الشروط (BoundaryCondition) ─── necessary/sufficient conditions
        │       ├── necessary_conditions   ─── شروط لازمة
        │       └── sufficient_conditions  ─── شروط كافية
        │
        └── فرع الهوية (identity_fields) ─── Identity(L0) ⊆ Identity(L1)

Every definition carries:
    - term: the defined entity name (المُعَرَّف)
    - genus: the broader class (الجنس)
    - differentia: what distinguishes it from siblings (الفصل)
    - boundary_conditions: necessary and sufficient conditions (الشروط الحدّية)
    - l0_source_ref: reference to the L0 entity file (المرجع)
    - identity_fields: fields preserved from L0 → L1 (حفظ الهوية)

This follows the classical Arabic definition method (حد):
    التعريف = الجنس + الفصل
    (Definition = Genus + Differentia)
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
class DefinitionCategory(str, Enum):
    """Categories of L1 formal definitions — فروع التصنيف.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §2 (Four Priority Categories)

    Each category groups related definitions that share structural properties:
    - PHONOLOGICAL: entities grounded in sound (الصوت)
    - COMPOSITIONAL: entities formed by combining phonological units (التركيب)
    - SEMANTIC: entities relating form to meaning (الدلالة)
    - STRUCTURAL: entities governing weight and boundaries (البنية)
    """

    PHONOLOGICAL = "phonological"
    COMPOSITIONAL = "compositional"
    SEMANTIC = "semantic"
    STRUCTURAL = "structural"


# ══════════════════════════════════════════════════════════════════════════════
# §2  BOUNDARY CONDITIONS (شروط حدّية)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class BoundaryCondition:
    """A formal boundary condition for a definition — شرط حدّي.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §6 L1

    A boundary condition specifies what must hold (necessary) or what is
    enough to confirm (sufficient) for an entity to be well-formed.

    Parameters
    ----------
    condition_id : str
        Unique identifier for this condition (e.g. "BC-PHONEME-01").
    description : str
        Human-readable description of the condition.
    is_necessary : bool
        Whether this is a necessary condition (شرط لازم).
    is_sufficient : bool
        Whether this is a sufficient condition (شرط كافٍ).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    condition_id: str
    description: str
    is_necessary: bool
    is_sufficient: bool
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §6 L1"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.condition_id:
            raise ValueError(FailureCode.M_01_08.value)
        if not self.description:
            raise ValueError(FailureCode.M_01_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)


# ══════════════════════════════════════════════════════════════════════════════
# §3  THE ROOT — FormalDefinition (الأصل)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class FormalDefinition:
    """The root of all L1 formal definitions — الأصل.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §6 L1 (Formal Description)

    Every formal definition follows the classical Arabic method (حد):
        التعريف = الجنس + الفصل
        Definition = Genus + Differentia

    This is the أصل (root) from which all فروع (branches) derive.
    Each branch specializes via:
        - category: which group it belongs to (DefinitionCategory)
        - boundary_conditions: what makes it well-formed
        - identity_fields: what is preserved from L0

    Parameters
    ----------
    term : str
        The defined entity name (المُعَرَّف) — e.g. "PhonemeUnit".
    genus : str
        The broader class (الجنس) — e.g. "phonological unit".
    differentia : str
        What distinguishes it (الفصل) — e.g. "single consonant + pattern".
    category : DefinitionCategory
        Which branch category this definition belongs to.
    l0_source_ref : str
        Reference to the L0 entity file (e.g. "L0/phoneme.py").
    constitution_ref : str
        Reference to the relevant constitution section.
    boundary_conditions : Tuple[BoundaryCondition, ...]
        Necessary and sufficient conditions for well-formedness.
    identity_fields : FrozenSet[str]
        Field names preserved from L0 → L1 (Identity(L0) ⊆ Identity(L1)).
    closed_set_size : int
        Size of the closed set this entity belongs to (0 if not a closed set).
    trace_ref : str
        Constitutional reference for this definition itself.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    term: str
    genus: str
    differentia: str
    category: DefinitionCategory
    l0_source_ref: str
    constitution_ref: str
    boundary_conditions: Tuple[BoundaryCondition, ...]
    identity_fields: FrozenSet[str]
    closed_set_size: int = 0
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §6 L1"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Birth guard — validates all definition fields."""
        if not self.term:
            raise ValueError(FailureCode.M_01_02.value)
        if not self.genus:
            raise ValueError(FailureCode.M_01_08.value)
        if not self.differentia:
            raise ValueError(FailureCode.M_01_08.value)
        if not isinstance(self.category, DefinitionCategory):
            raise ValueError(FailureCode.M_01_08.value)
        if not self.l0_source_ref:
            raise ValueError(FailureCode.M_01_02.value)
        if not self.constitution_ref:
            raise ValueError(FailureCode.M_01_03.value)
        if not isinstance(self.boundary_conditions, tuple):
            raise ValueError(FailureCode.M_01_08.value)
        if not self.identity_fields:
            raise ValueError(FailureCode.M_01_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)
        if self.closed_set_size < 0:
            raise ValueError(FailureCode.M_01_08.value)


# ══════════════════════════════════════════════════════════════════════════════
# §4  THE BRANCHES — Formal Definitions for All 13 L0 Entities (الفروع)
# ══════════════════════════════════════════════════════════════════════════════


# ── Branch 1: PHONOLOGICAL Category ─────────────────────────────────────────

DEF_PHONEME = FormalDefinition(
    term="PhonemeUnit",
    genus="phonological unit",
    differentia="single consonant carrier bound to exactly one of 8 phonetic patterns",
    category=DefinitionCategory.PHONOLOGICAL,
    l0_source_ref="L0/phoneme.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §3 (MCE-1)",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-PHONEME-01",
            description="consonant must be a non-empty string of at most 4 characters",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-PHONEME-02",
            description="pattern must be one of exactly 8 PhoneticPattern values",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"consonant", "pattern", "trace_ref", "rank", "residuals"}),
    closed_set_size=8,
)

DEF_GRAPHEME = FormalDefinition(
    term="Grapheme",
    genus="phonological unit",
    differentia="one of exactly 28 Arabic letters with articulation point and manner",
    category=DefinitionCategory.PHONOLOGICAL,
    l0_source_ref="L0/grapheme.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-GRAPHEME-01",
            description="letter must be a member of the closed 28-letter GRAPHEME_TABLE",
            is_necessary=True,
            is_sufficient=True,
        ),
        BoundaryCondition(
            condition_id="BC-GRAPHEME-02",
            description="articulation_point and manner must be non-empty",
            is_necessary=True,
            is_sufficient=False,
        ),
    ),
    identity_fields=frozenset({"letter", "articulation_point", "manner", "trace_ref", "rank", "residuals"}),
    closed_set_size=28,
)

DEF_VOWEL = FormalDefinition(
    term="Vowel",
    genus="phonological unit",
    differentia="one of exactly 7 vowels (4 short + 3 madd) from a closed enumeration",
    category=DefinitionCategory.PHONOLOGICAL,
    l0_source_ref="L0/vowel.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-VOWEL-01",
            description="value must be a member of the Vowel enum (7 members)",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"value", "trace_ref", "rank", "residuals"}),
    closed_set_size=7,
)

DEF_SYLLABLE = FormalDefinition(
    term="Syllable",
    genus="phonological unit",
    differentia="ordered sequence of PhonemeUnits conforming to one of 4 syllable types (CV, CVC, CVV, CVCC)",
    category=DefinitionCategory.PHONOLOGICAL,
    l0_source_ref="L0/syllable.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2)",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-SYLLABLE-01",
            description="phoneme sequence must be non-empty",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-SYLLABLE-02",
            description="syllable_type must be one of exactly 4 SyllableType values",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-SYLLABLE-03",
            description="phoneme sequence length must match syllable type pattern",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"phonemes", "syllable_type", "trace_ref", "rank", "residuals"}),
    closed_set_size=4,
)

# ── Branch 2: COMPOSITIONAL Category ────────────────────────────────────────

DEF_UTTERANCE = FormalDefinition(
    term="Utterance",
    genus="compositional unit",
    differentia="ordered non-empty sequence of Syllables forming a phonological word",
    category=DefinitionCategory.COMPOSITIONAL,
    l0_source_ref="L0/utterance.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-UTTERANCE-01",
            description="syllable sequence must be non-empty",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"syllables", "trace_ref", "rank", "residuals"}),
)

DEF_SIGNIFIER = FormalDefinition(
    term="Signifier",
    genus="compositional unit",
    differentia="licensed Utterance validated for phonological well-formedness per P1 (Sound Primacy)",
    category=DefinitionCategory.COMPOSITIONAL,
    l0_source_ref="L0/signifier.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P1",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-SIGNIFIER-01",
            description="must be grounded in a valid Utterance",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-SIGNIFIER-02",
            description="must carry a license_ref proving phonological licensing",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"utterance", "license_ref", "trace_ref", "rank", "residuals"}),
)

DEF_SIGNIFIED = FormalDefinition(
    term="LinguisticSignified",
    genus="compositional unit",
    differentia="intra-systemic linguistic content placeholder awaiting L1 bridge for full semantics",
    category=DefinitionCategory.COMPOSITIONAL,
    l0_source_ref="L0/signified.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (LinguisticSignified)",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-SIGNIFIED-01",
            description="concept_label must be non-empty",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"concept_label", "trace_ref", "rank", "residuals"}),
)

DEF_UNION = FormalDefinition(
    term="Union",
    genus="compositional unit",
    differentia="pairing of Signifier and ConventionalSignified forming the complete sign in L0",
    category=DefinitionCategory.COMPOSITIONAL,
    l0_source_ref="L0/union.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-UNION-01",
            description="signifier must be a valid Signifier instance",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-UNION-02",
            description="signified must be a valid ConventionalSignified instance",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"signifier", "signified", "trace_ref", "rank", "residuals"}),
)

# ── Branch 3: SEMANTIC Category ─────────────────────────────────────────────

DEF_SIGNIFICATION = FormalDefinition(
    term="Signification",
    genus="semantic relation",
    differentia="typed relation (5 types: kulliyy, juziyy, mutabaqa, tadmin, iltizam) between signifier and signified",
    category=DefinitionCategory.SEMANTIC,
    l0_source_ref="L0/signification.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-SIGNIFICATION-01",
            description="signification_type must be one of exactly 5 SignificationType values",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-SIGNIFICATION-02",
            description="must reference both a signifier and a signified",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"signification_type", "signifier", "signified", "trace_ref", "rank", "residuals"}),
    closed_set_size=5,
)

DEF_JAMID = FormalDefinition(
    term="JamidAnchor",
    genus="semantic relation",
    differentia="immutable lexical anchor (binary: 4 anchors, ternary: 3 anchors) that is NEVER a derivational root",
    category=DefinitionCategory.SEMANTIC,
    l0_source_ref="L0/jamid.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2; docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-05",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-JAMID-01",
            description="anchor_type must be BINARY or TERNARY",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-JAMID-02",
            description="phoneme sequence length must match anchor_type (2 for binary, 3 for ternary)",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-JAMID-03",
            description="anchor must be from the closed set (4 binary + 3 ternary = 7 total)",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"anchor_type", "phonemes", "trace_ref", "rank", "residuals"}),
    closed_set_size=7,
)

DEF_HARF_MAANI = FormalDefinition(
    term="HarfMaani",
    genus="semantic relation",
    differentia="Arabic particle (one of 20 canonical forms) carrying grammatical function, mostly sukun-based",
    category=DefinitionCategory.SEMANTIC,
    l0_source_ref="L0/harf_maani.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-HARF-01",
            description="phonetic_form must be non-empty",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-HARF-02",
            description="function must be non-empty (no particle without function: M_00_08)",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-HARF-03",
            description="must be a member of the 20-element HARF_MAANI_TABLE",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"phonetic_form", "function", "trace_ref", "rank", "residuals"}),
    closed_set_size=20,
)

# ── Branch 4: STRUCTURAL Category ───────────────────────────────────────────

DEF_WEIGHT = FormalDefinition(
    term="WeightUnit",
    genus="structural unit",
    differentia="weight pattern assignment (ROOT + 8 augmented forms = 9 patterns) licensing candidates but NOT producing meaning",
    category=DefinitionCategory.STRUCTURAL,
    l0_source_ref="L0/weight.py",
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P4 (No Meaning from Weight)",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-WEIGHT-01",
            description="pattern must be one of exactly 9 WeightPattern values",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-WEIGHT-02",
            description="weight does NOT produce meaning — only licensed candidates (P4)",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-WEIGHT-03",
            description="root consonants must be present and valid",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"pattern", "root", "trace_ref", "rank", "residuals"}),
    closed_set_size=9,
)

DEF_WAQF_WASL = FormalDefinition(
    term="WaqfWaslProfile",
    genus="structural unit",
    differentia="complete stopping/joining profile across 4 boundary levels (phonetic, structural, functional, semantic)",
    category=DefinitionCategory.STRUCTURAL,
    l0_source_ref="L0/waqf_wasl.py",
    constitution_ref="docs/20_WAQF_WASL_BOUNDARY_THEOREM.md TH6.5",
    boundary_conditions=(
        BoundaryCondition(
            condition_id="BC-WAQF-01",
            description="must specify boundary tests across all 4 levels",
            is_necessary=True,
            is_sufficient=False,
        ),
        BoundaryCondition(
            condition_id="BC-WAQF-02",
            description="each boundary level must have a valid WaqfStatus",
            is_necessary=True,
            is_sufficient=True,
        ),
    ),
    identity_fields=frozenset({"word_path", "boundary_tests", "trace_ref", "rank", "residuals"}),
    closed_set_size=4,
)


# ══════════════════════════════════════════════════════════════════════════════
# §5  REGISTRY — All 13 Definitions (السجل الكامل)
# ══════════════════════════════════════════════════════════════════════════════


FORMAL_DEFINITIONS: Tuple[FormalDefinition, ...] = (
    DEF_PHONEME,
    DEF_GRAPHEME,
    DEF_VOWEL,
    DEF_SYLLABLE,
    DEF_UTTERANCE,
    DEF_SIGNIFIER,
    DEF_SIGNIFIED,
    DEF_UNION,
    DEF_SIGNIFICATION,
    DEF_JAMID,
    DEF_HARF_MAANI,
    DEF_WEIGHT,
    DEF_WAQF_WASL,
)

# Indexed by term name for lookup
DEFINITION_BY_TERM: Dict[str, FormalDefinition] = {
    d.term: d for d in FORMAL_DEFINITIONS
}


# ══════════════════════════════════════════════════════════════════════════════
# §6  PURE FUNCTIONS — Definition Utilities
# ══════════════════════════════════════════════════════════════════════════════


def get_definition(term: str) -> FormalDefinition:
    """Retrieve a formal definition by its term name.

    Parameters
    ----------
    term : str
        The entity name (e.g. "PhonemeUnit").

    Returns
    -------
    FormalDefinition
        The formal definition for the given term.

    Raises
    ------
    ValueError
        If the term is not found (M_01_02).
    """
    if term not in DEFINITION_BY_TERM:
        raise ValueError(FailureCode.M_01_02.value)
    return DEFINITION_BY_TERM[term]


def definitions_by_category(category: DefinitionCategory) -> Tuple[FormalDefinition, ...]:
    """Retrieve all definitions belonging to a given category.

    Parameters
    ----------
    category : DefinitionCategory
        The category to filter by.

    Returns
    -------
    Tuple[FormalDefinition, ...]
        All definitions in the given category.
    """
    return tuple(d for d in FORMAL_DEFINITIONS if d.category == category)


def verify_identity_preservation(definition: FormalDefinition, l0_fields: FrozenSet[str]) -> bool:
    """Verify that Identity(L0) is a subset of Identity(L1) for a definition.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7

    Parameters
    ----------
    definition : FormalDefinition
        The L1 definition to verify.
    l0_fields : FrozenSet[str]
        The set of identity fields from the L0 entity.

    Returns
    -------
    bool
        True if identity is preserved (l0_fields is subset of definition.identity_fields).

    Raises
    ------
    ValueError
        If identity is not preserved (M_01_20).
    """
    if not l0_fields.issubset(definition.identity_fields):
        missing = l0_fields - definition.identity_fields
        raise ValueError(
            f"{FailureCode.M_01_20.value}: "
            f"Identity fields lost in L0→L1 for {definition.term}: {missing}"
        )
    return True


def total_definition_count() -> int:
    """Return the total number of formal definitions in the registry.

    Returns
    -------
    int
        Should be 13 (matching L0 entity count).
    """
    return len(FORMAL_DEFINITIONS)
