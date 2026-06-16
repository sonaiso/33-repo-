"""
Waqf-Wasl Boundary Economy — TH6.5 implementation.
Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md; docs/00_MAQOOL_CONSTITUTION.md §4, §5

This module implements the Waqf-Wasl Boundary Economy Theorem (TH6.5):
- Waqf (الوقف) = boundary closure test at a given level
- Wasl (الوصل) = declaration of need for complement at a given level
- Economy Law = no structure higher than what the minimum boundary requires

The theorem establishes that stopping/connection must be tested before weight (TH7)
can apply, and that phonetic closure ≠ structural closure ≠ semantic closure.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


# ══════════════════════════════════════════════════════════════════════════════
# §1  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════


@unique
class BoundaryLevel(str, Enum):
    """The four levels at which waqf/wasl is tested.

    Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §4
    """

    PHONETIC = "phonetic"        # هل يمكن النطق والتوقف؟
    STRUCTURAL = "structural"    # هل اكتملت بنية اللفظ/الكلمة؟
    FUNCTIONAL = "functional"    # هل يعمل وحده أم يحتاج متعلقًا؟
    SEMANTIC = "semantic"        # هل تحقق معنى مكتمل؟


@unique
class WordPath(str, Enum):
    """The functional path a word may take after boundary testing.

    Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §6
    """

    ISM_MUTAMAKKIN = "ism_mutamakkin"    # اسم متمكن (full noun)
    ISM_MABNI = "ism_mabni"              # اسم مبني (built noun: demonstrative, relative, pronoun)
    FI_L_TAAM = "fi_l_taam"              # فعل تام (complete verb)
    FI_L_NAQIS = "fi_l_naqis"            # فعل ناقص (incomplete verb)
    HARF = "harf"                         # حرف (particle/operator)
    MABNI_OTHER = "mabni_other"          # مبني غير اسمي (other built form)


@unique
class WaqfStatus(str, Enum):
    """Result of a waqf (stopping) test at a given level.

    Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §3
    """

    CLOSED = "closed"    # الوقف صحيح — الحد مغلق
    OPEN = "open"        # يحتاج وصلًا — الحد مفتوح


# ══════════════════════════════════════════════════════════════════════════════
# §2  CORE ENTITIES
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class BoundaryTest:
    """A single boundary test result at one level for a linguistic unit.

    Records whether a unit can stop (waqf) or must join (wasl) at this level.

    Parameters
    ----------
    level : BoundaryLevel
        The level being tested.
    status : WaqfStatus
        CLOSED if waqf is valid, OPEN if wasl is required.
    required_complement : str
        Description of what is needed if OPEN (empty string if CLOSED).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    level: BoundaryLevel
    status: WaqfStatus
    required_complement: str = ""
    trace_ref: str = "docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §3"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if not isinstance(self.level, BoundaryLevel):
            raise ValueError(f"{FailureCode.M_CX_08.value}: invalid_boundary_level")
        if not isinstance(self.status, WaqfStatus):
            raise ValueError(f"{FailureCode.M_CX_08.value}: invalid_waqf_status")
        # If open, must declare what complement is required
        if self.status == WaqfStatus.OPEN and not self.required_complement:
            raise ValueError(
                f"{FailureCode.M_CX_08.value}: open_boundary_missing_complement"
            )


@dataclass(frozen=True)
class WaqfWaslProfile:
    """Complete waqf/wasl profile for a linguistic unit across all four levels.

    This is the primary entity of TH6.5: it encodes where a unit can stop
    and where it must join with another unit.

    Parameters
    ----------
    unit_label : str
        The label of the linguistic unit being tested (e.g. "min", "zayd", "kataba").
    word_path : WordPath
        The functional path this unit belongs to.
    tests : Tuple[BoundaryTest, ...]
        Boundary tests for each level (must cover all 4 levels).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    unit_label: str
    word_path: WordPath
    tests: Tuple[BoundaryTest, ...]
    domain_tag: str = "L0_WAQF_WASL"
    trace_ref: str = "docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §3"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.unit_label:
            raise ValueError(f"{FailureCode.M_CX_08.value}: unit_label_empty")
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if not isinstance(self.word_path, WordPath):
            raise ValueError(f"{FailureCode.M_CX_08.value}: invalid_word_path")
        if not self.tests:
            raise ValueError(f"{FailureCode.M_CX_08.value}: tests_empty")
        # Verify all four levels are covered
        levels_present = frozenset(t.level for t in self.tests)
        levels_required = frozenset(BoundaryLevel)
        if levels_present != levels_required:
            missing = levels_required - levels_present
            raise ValueError(
                f"{FailureCode.M_CX_08.value}: missing_boundary_levels: "
                f"{sorted(m.value for m in missing)}"
            )

    @property
    def can_stop_phonetic(self) -> bool:
        """Whether the unit can stop at the phonetic level."""
        return self.status_at(BoundaryLevel.PHONETIC) == WaqfStatus.CLOSED

    @property
    def can_stop_structural(self) -> bool:
        """Whether the unit can stop at the structural level."""
        return self.status_at(BoundaryLevel.STRUCTURAL) == WaqfStatus.CLOSED

    @property
    def can_stop_functional(self) -> bool:
        """Whether the unit can stop at the functional level."""
        return self.status_at(BoundaryLevel.FUNCTIONAL) == WaqfStatus.CLOSED

    @property
    def can_stop_semantic(self) -> bool:
        """Whether the unit can stop at the semantic level."""
        return self.status_at(BoundaryLevel.SEMANTIC) == WaqfStatus.CLOSED

    @property
    def must_join_levels(self) -> Tuple[BoundaryLevel, ...]:
        """Return all levels where this unit must join (wasl)."""
        return tuple(t.level for t in self.tests if t.status == WaqfStatus.OPEN)

    def status_at(self, level: BoundaryLevel) -> WaqfStatus:
        """Return the WaqfStatus for the given boundary level."""
        for t in self.tests:
            if t.level == level:
                return t.status
        raise ValueError(f"{FailureCode.M_CX_08.value}: level_not_found: {level.value}")


# ══════════════════════════════════════════════════════════════════════════════
# §3  PURE BOUNDARY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════


def can_stop(profile: WaqfWaslProfile, level: BoundaryLevel) -> bool:
    """Pure function: test whether a unit can stop at the given level.

    CanStop(x, level) ⇔ BoundaryClosed(x, level)

    Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §7
    """
    return profile.status_at(level) == WaqfStatus.CLOSED


def must_join(profile: WaqfWaslProfile, level: BoundaryLevel) -> bool:
    """Pure function: test whether a unit must join at the given level.

    MustJoin(x, level) ⇔ RequiredComplement(x, level) ≠ ∅

    Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §7
    """
    return profile.status_at(level) == WaqfStatus.OPEN


def required_complement_at(profile: WaqfWaslProfile, level: BoundaryLevel) -> str:
    """Pure function: return what complement is needed at the given level.

    Returns empty string if the boundary is closed (no complement needed).

    Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md §7
    """
    for t in profile.tests:
        if t.level == level:
            return t.required_complement
    raise ValueError(f"{FailureCode.M_CX_08.value}: level_not_found: {level.value}")


# ══════════════════════════════════════════════════════════════════════════════
# §4  ECONOMY GUARD FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════


def guard_no_weight_before_word(
    has_word_boundary: bool,
    attempting_weight: bool,
) -> None:
    """Guard WW-03: No weight before word boundary is established.

    Raises
    ------
    ValueError
        With FailureCode.M_WW_01 if weight is attempted before word boundary.
    """
    if attempting_weight and not has_word_boundary:
        raise ValueError(
            f"{FailureCode.M_WW_01.value}: "
            "weight cannot be applied before word boundary is established (WW-03)"
        )


def guard_no_word_before_syllable(
    has_syllable_license: bool,
    attempting_word: bool,
) -> None:
    """Guard WW-04: No word before syllable license is established.

    Raises
    ------
    ValueError
        With FailureCode.M_WW_02 if word is attempted before syllable license.
    """
    if attempting_word and not has_syllable_license:
        raise ValueError(
            f"{FailureCode.M_WW_02.value}: "
            "word cannot be established before syllable license (WW-04)"
        )


def guard_no_semantic_without_relation(
    claiming_complete_meaning: bool,
    has_licensed_relation: bool,
) -> None:
    """Guard WW-14/P38: No complete meaning from a single word without relation.

    Raises
    ------
    ValueError
        With FailureCode.M_WW_03 if semantic closure is claimed without relation.
    """
    if claiming_complete_meaning and not has_licensed_relation:
        raise ValueError(
            f"{FailureCode.M_WW_03.value}: "
            "complete meaning requires a licensed relation, not a single word (WW-14)"
        )


def guard_harf_has_operand(
    word_path: WordPath,
    has_operand: bool,
) -> None:
    """Guard WW-10: Particle must have an operand (must join obligatorily).

    Raises
    ------
    ValueError
        With FailureCode.M_WW_04 if a harf lacks an operand.
    """
    if word_path == WordPath.HARF and not has_operand:
        raise ValueError(
            f"{FailureCode.M_WW_04.value}: "
            "particle (harf) must join with its operand (WW-10)"
        )


def guard_incomplete_verb_has_complement(
    word_path: WordPath,
    has_complement: bool,
) -> None:
    """Guard WW-09: Incomplete verb must have complement.

    Raises
    ------
    ValueError
        With FailureCode.M_WW_05 if an incomplete verb lacks complement.
    """
    if word_path == WordPath.FI_L_NAQIS and not has_complement:
        raise ValueError(
            f"{FailureCode.M_WW_05.value}: "
            "incomplete verb (fi'l naqis) must join with its complement (WW-09)"
        )


def guard_sub_ternary_not_in_weight(
    consonant_count: int,
    attempting_derivational_weight: bool,
) -> None:
    """Guard WW-15: Sub-ternary cannot enter derivational weight.

    Raises
    ------
    ValueError
        With FailureCode.M_WW_06 if sub-ternary attempts derivational weight.
    """
    if consonant_count < 3 and attempting_derivational_weight:
        raise ValueError(
            f"{FailureCode.M_WW_06.value}: "
            "sub-ternary unit cannot enter derivational weight path (WW-15)"
        )


def guard_phonetic_stop_not_meaning(
    can_stop_phonetic: bool,
    claiming_meaning_from_stop: bool,
) -> None:
    """Guard WW-01/WW-07: Phonetic stop ≠ complete meaning.

    Raises
    ------
    ValueError
        With FailureCode.M_WW_07 if phonetic stop is claimed as meaning.
    """
    if can_stop_phonetic and claiming_meaning_from_stop:
        raise ValueError(
            f"{FailureCode.M_WW_07.value}: "
            "phonetic stop is a closure test, not proof of complete meaning (WW-01)"
        )


def guard_structural_stop_not_ifadah(
    can_stop_structural: bool,
    claiming_ifadah_from_structure: bool,
) -> None:
    """Guard WW-01/WW-08: Structural stop ≠ complete ifadah.

    Raises
    ------
    ValueError
        With FailureCode.M_WW_08 if structural stop is claimed as ifadah.
    """
    if can_stop_structural and claiming_ifadah_from_structure:
        raise ValueError(
            f"{FailureCode.M_WW_08.value}: "
            "structural stop is not proof of complete ifadah (WW-01)"
        )


# ══════════════════════════════════════════════════════════════════════════════
# §5  CANONICAL PROFILES
# ══════════════════════════════════════════════════════════════════════════════


def _bt(level: BoundaryLevel, status: WaqfStatus, complement: str = "") -> BoundaryTest:
    """Helper to build BoundaryTest concisely."""
    return BoundaryTest(level=level, status=status, required_complement=complement)


# ── Harf (particle) profile: "min" (من) ─────────────────────────────────────
PROFILE_MIN = WaqfWaslProfile(
    unit_label="min",
    word_path=WordPath.HARF,
    tests=(
        _bt(BoundaryLevel.PHONETIC, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.STRUCTURAL, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.FUNCTIONAL, WaqfStatus.OPEN, "majrur (مجرور)"),
        _bt(BoundaryLevel.SEMANTIC, WaqfStatus.OPEN, "muta'allaq (متعلَّق)"),
    ),
)

# ── Ism mutamakkin profile: "rajul" (رجل) ───────────────────────────────────
PROFILE_RAJUL = WaqfWaslProfile(
    unit_label="rajul",
    word_path=WordPath.ISM_MUTAMAKKIN,
    tests=(
        _bt(BoundaryLevel.PHONETIC, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.STRUCTURAL, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.FUNCTIONAL, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.SEMANTIC, WaqfStatus.OPEN, "tarkib li-l-ifadah (تركيب للإفادة)"),
    ),
)

# ── Fi'l taam profile: "kataba" (كتب) ───────────────────────────────────────
PROFILE_KATABA = WaqfWaslProfile(
    unit_label="kataba",
    word_path=WordPath.FI_L_TAAM,
    tests=(
        _bt(BoundaryLevel.PHONETIC, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.STRUCTURAL, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.FUNCTIONAL, WaqfStatus.OPEN, "fa'il (فاعل)"),
        _bt(BoundaryLevel.SEMANTIC, WaqfStatus.OPEN, "musnad ilayh (مسند إليه)"),
    ),
)

# ── Fi'l naqis profile: "kana" (كان) ────────────────────────────────────────
PROFILE_KANA = WaqfWaslProfile(
    unit_label="kana",
    word_path=WordPath.FI_L_NAQIS,
    tests=(
        _bt(BoundaryLevel.PHONETIC, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.STRUCTURAL, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.FUNCTIONAL, WaqfStatus.OPEN, "ism wa-khabar (اسم وخبر)"),
        _bt(BoundaryLevel.SEMANTIC, WaqfStatus.OPEN, "ism wa-khabar (اسم وخبر)"),
    ),
)

# ── Ism mabni profile: "hadha" (هذا) ────────────────────────────────────────
PROFILE_HADHA = WaqfWaslProfile(
    unit_label="hadha",
    word_path=WordPath.ISM_MABNI,
    tests=(
        _bt(BoundaryLevel.PHONETIC, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.STRUCTURAL, WaqfStatus.CLOSED),
        _bt(BoundaryLevel.FUNCTIONAL, WaqfStatus.OPEN, "mushaar ilayh (مشار إليه)"),
        _bt(BoundaryLevel.SEMANTIC, WaqfStatus.OPEN, "maqam aw mushaar ilayh (مقام أو مشار إليه)"),
    ),
)


# All canonical profiles for testing
CANONICAL_PROFILES: Tuple[WaqfWaslProfile, ...] = (
    PROFILE_MIN,
    PROFILE_RAJUL,
    PROFILE_KATABA,
    PROFILE_KANA,
    PROFILE_HADHA,
)
