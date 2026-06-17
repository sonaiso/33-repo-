"""
MarkRegistry — Arabic diacritical marks (harakat) as licensed operators.

A haraka is an operator (مشغّل), not an independent carrier.
It operates on a letter without changing the letter's identity.

Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Vowel)
trace_ref: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §MarkRegistry

Laws:
- Haraka is an operator, not an independent carrier (الحركة مشغّل لا حامل مستقل)
- Sukun closes the letter without erasing identity (السكون يغلق ولا يمحو)
- Shadda doubles functionally without creating new identity (الشدة تضاعف ولا تخلق)
- Tanwin is haraka + nunnation effect (التنوين حركة مع أثر نوني)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class MarkGenus(str, Enum):
    """Genus classification for Arabic diacritical marks.

    Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §MarkRegistry
    """

    SHORT_VOWEL = "short_vowel_operator"
    SUKUN = "sukun_operator"
    SHADDA = "shadda_operator"
    TANWIN = "tanwin_operator"
    MADD_SIGN = "madd_sign"
    SUPERSCRIPT_ALIF = "superscript_alif"


class MarkFunction(str, Enum):
    """Functional role of a diacritical mark.

    Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §MarkRegistry
    """

    VOWEL_OPEN = "vowel_open"           # فتح الحرف صوتيًا
    VOWEL_ROUND = "vowel_round"         # ضم الحرف صوتيًا
    VOWEL_FRONT = "vowel_front"         # كسر الحرف صوتيًا
    CLOSE_LETTER = "close_letter"       # إغلاق الحرف بلا حركة
    GEMINATE = "geminate"               # تضعيف الحرف وظيفيًا
    VOWEL_NUNNATION = "vowel_nunnation" # حركة + أثر نوني
    EXTEND = "extend"                   # تطويل/امتداد


@dataclass(frozen=True)
class MarkIdentity:
    """A single Arabic diacritical mark with its operator identity.

    A mark is always an operator — it acts upon a letter carrier.
    It never stands independently as a carrier of meaning.

    Parameters
    ----------
    mark_id : str
        Canonical identifier (e.g. "FATHA", "SHADDA").
    unicode_codepoint : str
        Unicode codepoint (e.g. "U+064E").
    glyph : str
        The mark character.
    genus : MarkGenus
        Classification of the mark.
    function : MarkFunction
        What the mark does to its host letter.
    attaches_to : str
        What kind of carrier this mark attaches to.
    opens_next_layer : str
        What layer/structure this enables.
    preventers : FrozenSet[str]
        What conditions prevent this mark from attaching.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    mark_id: str
    unicode_codepoint: str
    glyph: str
    genus: MarkGenus
    function: MarkFunction
    attaches_to: str
    opens_next_layer: str
    preventers: FrozenSet[str]
    trace_ref: str = "docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §MarkRegistry"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.mark_id:
            raise ValueError(
                f"{FailureCode.M_00_04.value}: mark_id cannot be empty"
            )
        if not self.unicode_codepoint:
            raise ValueError(
                f"{FailureCode.M_00_04.value}: unicode_codepoint cannot be empty"
            )
        if not isinstance(self.genus, MarkGenus):
            raise ValueError(
                f"{FailureCode.M_00_04.value}: genus must be a MarkGenus member"
            )
        if not isinstance(self.function, MarkFunction):
            raise ValueError(
                f"{FailureCode.M_00_04.value}: function must be a MarkFunction member"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ── Canonical mark registry ──────────────────────────────────────────────────

MARK_REGISTRY: Tuple[MarkIdentity, ...] = (
    MarkIdentity(
        mark_id="FATHA",
        unicode_codepoint="U+064E",
        glyph="\u064E",
        genus=MarkGenus.SHORT_VOWEL,
        function=MarkFunction.VOWEL_OPEN,
        attaches_to="letter_carrier",
        opens_next_layer="CV syllable candidate",
        preventers=frozenset({"conflicting_short_vowel", "sukun_present"}),
    ),
    MarkIdentity(
        mark_id="DAMMA",
        unicode_codepoint="U+064F",
        glyph="\u064F",
        genus=MarkGenus.SHORT_VOWEL,
        function=MarkFunction.VOWEL_ROUND,
        attaches_to="letter_carrier",
        opens_next_layer="CV syllable candidate",
        preventers=frozenset({"conflicting_short_vowel", "sukun_present"}),
    ),
    MarkIdentity(
        mark_id="KASRA",
        unicode_codepoint="U+0650",
        glyph="\u0650",
        genus=MarkGenus.SHORT_VOWEL,
        function=MarkFunction.VOWEL_FRONT,
        attaches_to="letter_carrier",
        opens_next_layer="CV syllable candidate",
        preventers=frozenset({"conflicting_short_vowel", "sukun_present"}),
    ),
    MarkIdentity(
        mark_id="SUKUN",
        unicode_codepoint="U+0652",
        glyph="\u0652",
        genus=MarkGenus.SUKUN,
        function=MarkFunction.CLOSE_LETTER,
        attaches_to="letter_carrier",
        opens_next_layer="closed consonant (coda candidate)",
        preventers=frozenset({"conflicting_short_vowel", "shadda_without_vowel"}),
    ),
    MarkIdentity(
        mark_id="SHADDA",
        unicode_codepoint="U+0651",
        glyph="\u0651",
        genus=MarkGenus.SHADDA,
        function=MarkFunction.GEMINATE,
        attaches_to="letter_carrier",
        opens_next_layer="geminated unit (requires follow-up vowel/sukun)",
        preventers=frozenset({"letter_does_not_accept_shadda"}),
    ),
    MarkIdentity(
        mark_id="FATHATAN",
        unicode_codepoint="U+064B",
        glyph="\u064B",
        genus=MarkGenus.TANWIN,
        function=MarkFunction.VOWEL_NUNNATION,
        attaches_to="letter_carrier",
        opens_next_layer="tanwin unit (haraka + nunnation)",
        preventers=frozenset({"conflicting_short_vowel", "definite_article_present"}),
    ),
    MarkIdentity(
        mark_id="DAMMATAN",
        unicode_codepoint="U+064C",
        glyph="\u064C",
        genus=MarkGenus.TANWIN,
        function=MarkFunction.VOWEL_NUNNATION,
        attaches_to="letter_carrier",
        opens_next_layer="tanwin unit (haraka + nunnation)",
        preventers=frozenset({"conflicting_short_vowel", "definite_article_present"}),
    ),
    MarkIdentity(
        mark_id="KASRATAN",
        unicode_codepoint="U+064D",
        glyph="\u064D",
        genus=MarkGenus.TANWIN,
        function=MarkFunction.VOWEL_NUNNATION,
        attaches_to="letter_carrier",
        opens_next_layer="tanwin unit (haraka + nunnation)",
        preventers=frozenset({"conflicting_short_vowel", "definite_article_present"}),
    ),
    MarkIdentity(
        mark_id="MADDAH",
        unicode_codepoint="U+0653",
        glyph="\u0653",
        genus=MarkGenus.MADD_SIGN,
        function=MarkFunction.EXTEND,
        attaches_to="alif_seat",
        opens_next_layer="madd unit (extended vowel)",
        preventers=frozenset({"non_alif_base"}),
    ),
    MarkIdentity(
        mark_id="SUPERSCRIPT_ALIF",
        unicode_codepoint="U+0670",
        glyph="\u0670",
        genus=MarkGenus.SUPERSCRIPT_ALIF,
        function=MarkFunction.EXTEND,
        attaches_to="letter_carrier",
        opens_next_layer="implied alif (orthographic variant)",
        preventers=frozenset(),
        residuals=frozenset({"orthographic_variant_ambiguity"}),
    ),
)

# ── Index maps ────────────────────────────────────────────────────────────────

MARK_BY_ID: dict[str, MarkIdentity] = {
    m.mark_id: m for m in MARK_REGISTRY
}

MARK_BY_CODEPOINT: dict[str, MarkIdentity] = {
    m.unicode_codepoint: m for m in MARK_REGISTRY
}


def get_mark_by_id(mark_id: str) -> MarkIdentity:
    """Pure lookup: return MarkIdentity by canonical ID.

    Raises
    ------
    ValueError
        With FailureCode.M_00_04 if mark_id is not found.
    """
    try:
        return MARK_BY_ID[mark_id]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_00_04.value}: mark_id {mark_id!r} not in registry"
        )


def get_mark_by_codepoint(codepoint: str) -> MarkIdentity:
    """Pure lookup: return MarkIdentity by Unicode codepoint.

    Raises
    ------
    ValueError
        With FailureCode.M_00_04 if codepoint is not found.
    """
    try:
        return MARK_BY_CODEPOINT[codepoint]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_00_04.value}: codepoint {codepoint!r} not in registry"
        )
