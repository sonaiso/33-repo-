"""
LetterRegistry — 28 Arabic letters as licensed digital identity carriers.

Each letter preserves its identity independently of any haraka or operator.
The letter is a silent identity carrier (حامل هوية صامتة).

Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Grapheme)
trace_ref: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §LetterRegistry

Laws:
- The letter preserves silent identity (الحرف يحفظ الهوية الصامتة)
- The haraka does not change letter identity (الحركة لا تغيّر هوية الحرف)
- Unicode witnesses orthography, not sound alone (اليونيكود يشهد على الرسم)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class LetterGenus(str, Enum):
    """Genus classification for Arabic letters.

    Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §LetterRegistry
    """

    CONSONANTAL = "consonantal_letter"
    LONG_VOWEL = "long_vowel_letter"
    HAMZA = "hamza"
    ALIF_SEAT = "alif_seat"


@dataclass(frozen=True)
class LetterIdentity:
    """A single Arabic letter with its digital identity properties.

    The letter is the silent identity carrier. Its identity is preserved
    regardless of what haraka, shadda, or sukun attaches to it.

    Parameters
    ----------
    letter_id : str
        Canonical identifier (e.g. "BA", "MEEM").
    unicode_codepoint : str
        Unicode codepoint (e.g. "U+0628").
    glyph : str
        The Arabic character (e.g. "ب").
    genus : LetterGenus
        Classification of the letter.
    essence : str
        The preserved identity description.
    accepts_haraka : bool
        Whether this letter can receive a short vowel.
    accepts_sukun : bool
        Whether this letter can receive sukun.
    accepts_shadda : bool
        Whether this letter can receive shadda (gemination).
    connects_right : bool
        Whether this letter connects to the right in script.
    connects_left : bool
        Whether this letter connects to the left in script.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    letter_id: str
    unicode_codepoint: str
    glyph: str
    genus: LetterGenus
    essence: str
    accepts_haraka: bool
    accepts_sukun: bool
    accepts_shadda: bool
    connects_right: bool
    connects_left: bool
    trace_ref: str = "docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §LetterRegistry"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.letter_id:
            raise ValueError(
                f"{FailureCode.M_00_03.value}: letter_id cannot be empty"
            )
        if not self.unicode_codepoint:
            raise ValueError(
                f"{FailureCode.M_00_03.value}: unicode_codepoint cannot be empty"
            )
        if not self.glyph:
            raise ValueError(
                f"{FailureCode.M_00_03.value}: glyph cannot be empty"
            )
        if not isinstance(self.genus, LetterGenus):
            raise ValueError(
                f"{FailureCode.M_00_03.value}: genus must be a LetterGenus member"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ── Canonical 28-letter registry ─────────────────────────────────────────────

LETTER_REGISTRY: Tuple[LetterIdentity, ...] = (
    LetterIdentity(
        letter_id="HAMZA", unicode_codepoint="U+0621", glyph="ء",
        genus=LetterGenus.HAMZA, essence="هوية الهمزة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=False,
        connects_right=False, connects_left=False,
    ),
    LetterIdentity(
        letter_id="BA", unicode_codepoint="U+0628", glyph="ب",
        genus=LetterGenus.CONSONANTAL, essence="هوية الباء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="TA", unicode_codepoint="U+062A", glyph="ت",
        genus=LetterGenus.CONSONANTAL, essence="هوية التاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="THA", unicode_codepoint="U+062B", glyph="ث",
        genus=LetterGenus.CONSONANTAL, essence="هوية الثاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="JEEM", unicode_codepoint="U+062C", glyph="ج",
        genus=LetterGenus.CONSONANTAL, essence="هوية الجيم الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="HAA", unicode_codepoint="U+062D", glyph="ح",
        genus=LetterGenus.CONSONANTAL, essence="هوية الحاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="KHAA", unicode_codepoint="U+062E", glyph="خ",
        genus=LetterGenus.CONSONANTAL, essence="هوية الخاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="DAL", unicode_codepoint="U+062F", glyph="د",
        genus=LetterGenus.CONSONANTAL, essence="هوية الدال الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=False,
    ),
    LetterIdentity(
        letter_id="DHAL", unicode_codepoint="U+0630", glyph="ذ",
        genus=LetterGenus.CONSONANTAL, essence="هوية الذال الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=False,
    ),
    LetterIdentity(
        letter_id="RA", unicode_codepoint="U+0631", glyph="ر",
        genus=LetterGenus.CONSONANTAL, essence="هوية الراء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=False,
    ),
    LetterIdentity(
        letter_id="ZAY", unicode_codepoint="U+0632", glyph="ز",
        genus=LetterGenus.CONSONANTAL, essence="هوية الزاي الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=False,
    ),
    LetterIdentity(
        letter_id="SEEN", unicode_codepoint="U+0633", glyph="س",
        genus=LetterGenus.CONSONANTAL, essence="هوية السين الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="SHEEN", unicode_codepoint="U+0634", glyph="ش",
        genus=LetterGenus.CONSONANTAL, essence="هوية الشين الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="SAAD", unicode_codepoint="U+0635", glyph="ص",
        genus=LetterGenus.CONSONANTAL, essence="هوية الصاد الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="DAAD", unicode_codepoint="U+0636", glyph="ض",
        genus=LetterGenus.CONSONANTAL, essence="هوية الضاد الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="TAA_EMPHATIC", unicode_codepoint="U+0637", glyph="ط",
        genus=LetterGenus.CONSONANTAL, essence="هوية الطاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="DHAA_EMPHATIC", unicode_codepoint="U+0638", glyph="ظ",
        genus=LetterGenus.CONSONANTAL, essence="هوية الظاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="AIN", unicode_codepoint="U+0639", glyph="ع",
        genus=LetterGenus.CONSONANTAL, essence="هوية العين الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="GHAIN", unicode_codepoint="U+063A", glyph="غ",
        genus=LetterGenus.CONSONANTAL, essence="هوية الغين الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="FA", unicode_codepoint="U+0641", glyph="ف",
        genus=LetterGenus.CONSONANTAL, essence="هوية الفاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="QAF", unicode_codepoint="U+0642", glyph="ق",
        genus=LetterGenus.CONSONANTAL, essence="هوية القاف الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="KAF", unicode_codepoint="U+0643", glyph="ك",
        genus=LetterGenus.CONSONANTAL, essence="هوية الكاف الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="LAM", unicode_codepoint="U+0644", glyph="ل",
        genus=LetterGenus.CONSONANTAL, essence="هوية اللام الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="MEEM", unicode_codepoint="U+0645", glyph="م",
        genus=LetterGenus.CONSONANTAL, essence="هوية الميم الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="NOON", unicode_codepoint="U+0646", glyph="ن",
        genus=LetterGenus.CONSONANTAL, essence="هوية النون الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="HA", unicode_codepoint="U+0647", glyph="ه",
        genus=LetterGenus.CONSONANTAL, essence="هوية الهاء الصامتة",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
    ),
    LetterIdentity(
        letter_id="WAW", unicode_codepoint="U+0648", glyph="و",
        genus=LetterGenus.LONG_VOWEL, essence="هوية الواو",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=False,
        residuals=frozenset({"madd_or_consonant_ambiguity"}),
    ),
    LetterIdentity(
        letter_id="YA", unicode_codepoint="U+064A", glyph="ي",
        genus=LetterGenus.LONG_VOWEL, essence="هوية الياء",
        accepts_haraka=True, accepts_sukun=True, accepts_shadda=True,
        connects_right=True, connects_left=True,
        residuals=frozenset({"madd_or_consonant_ambiguity"}),
    ),
)

assert len(LETTER_REGISTRY) == 28, (
    f"Expected 28 letters, got {len(LETTER_REGISTRY)}"
)

# ── Index maps for O(1) lookup ────────────────────────────────────────────────

LETTER_BY_ID: dict[str, LetterIdentity] = {
    lt.letter_id: lt for lt in LETTER_REGISTRY
}

LETTER_BY_GLYPH: dict[str, LetterIdentity] = {
    lt.glyph: lt for lt in LETTER_REGISTRY
}

LETTER_BY_CODEPOINT: dict[str, LetterIdentity] = {
    lt.unicode_codepoint: lt for lt in LETTER_REGISTRY
}


def get_letter_by_id(letter_id: str) -> LetterIdentity:
    """Pure lookup: return LetterIdentity by canonical ID.

    Raises
    ------
    ValueError
        With FailureCode.M_00_03 if letter_id is not found.
    """
    try:
        return LETTER_BY_ID[letter_id]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_00_03.value}: letter_id {letter_id!r} not in registry"
        )


def get_letter_by_glyph(glyph: str) -> LetterIdentity:
    """Pure lookup: return LetterIdentity by Arabic glyph.

    Raises
    ------
    ValueError
        With FailureCode.M_00_03 if glyph is not found.
    """
    try:
        return LETTER_BY_GLYPH[glyph]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_00_03.value}: glyph {glyph!r} not in registry"
        )


def get_letter_by_codepoint(codepoint: str) -> LetterIdentity:
    """Pure lookup: return LetterIdentity by Unicode codepoint.

    Raises
    ------
    ValueError
        With FailureCode.M_00_03 if codepoint is not found.
    """
    try:
        return LETTER_BY_CODEPOINT[codepoint]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_00_03.value}: codepoint {codepoint!r} not in registry"
        )
