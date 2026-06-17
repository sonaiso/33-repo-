"""
VocalizedParser — parse vocalized Arabic text into (letter, mark) pairs.

This module takes a fully vocalized Arabic string and decomposes it into
an ordered sequence of (LetterIdentity, Optional[MarkIdentity]) pairs.

It operates ONLY at the L0 level:
- It identifies letters and marks from the registries.
- It does NOT extract roots, weights, word classes, or any morphological info.
- Unvocalized text produces rank="deferred" with residuals={missing_harakat}.

Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedParser
trace_ref: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedParser
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Optional, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.letter_registry import (
    LETTER_BY_GLYPH,
    LetterIdentity,
)
from taaqqul_slot_geometry.core.mark_registry import (
    MARK_REGISTRY,
    MarkIdentity,
)


# ── Build glyph-based mark lookup ─────────────────────────────────────────────

MARK_BY_GLYPH: dict[str, MarkIdentity] = {
    m.glyph: m for m in MARK_REGISTRY
}

# Special characters: Alif (seat/carrier, not a consonant in the 28)
_ALIF_CODEPOINT = "\u0627"  # ا
_ALIF_HAMZA_ABOVE = "\u0623"  # أ
_ALIF_HAMZA_BELOW = "\u0625"  # إ
_ALIF_MADDA = "\u0622"  # آ
_TA_MARBUTA = "\u0629"  # ة

# Set of all special Alif seats
_ALIF_SEATS = frozenset({_ALIF_CODEPOINT, _ALIF_HAMZA_ABOVE, _ALIF_HAMZA_BELOW, _ALIF_MADDA})


@dataclass(frozen=True)
class ParsedUnit:
    """A single parsed unit: one letter with its optional attached mark.

    Parameters
    ----------
    letter : LetterIdentity
        The identified letter carrier.
    mark : Optional[MarkIdentity]
        The attached diacritical mark (None if no mark follows).
    is_alif_seat : bool
        Whether this position is an alif seat (not in the 28 letters).
    raw_letter : str
        The raw Unicode character for the letter.
    raw_mark : str
        The raw Unicode character for the mark (empty if none).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    letter: Optional[LetterIdentity]
    mark: Optional[MarkIdentity]
    is_alif_seat: bool
    raw_letter: str
    raw_mark: str
    trace_ref: str = "docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedParser"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.raw_letter:
            raise ValueError(
                f"{FailureCode.M_00_03.value}: raw_letter cannot be empty"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class ParseResult:
    """Result of parsing a vocalized Arabic string.

    Parameters
    ----------
    units : Tuple[ParsedUnit, ...]
        The ordered sequence of parsed (letter, mark) units.
    is_fully_vocalized : bool
        True if every letter has an attached mark.
        When False, residuals will contain "missing_harakat".
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE" (constitutional mandate).
    residuals : FrozenSet[str]
        Residual bundle. Contains "missing_harakat" if not fully vocalized.
    """

    units: Tuple[ParsedUnit, ...]
    is_fully_vocalized: bool
    trace_ref: str = "docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedParser"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


def _is_arabic_mark(char: str) -> bool:
    """Check if a character is an Arabic combining mark (pure function)."""
    return char in MARK_BY_GLYPH


def _is_arabic_letter(char: str) -> bool:
    """Check if a character is an Arabic letter in the registry (pure function)."""
    return char in LETTER_BY_GLYPH


def _is_alif_seat(char: str) -> bool:
    """Check if a character is an alif seat (pure function)."""
    return char in _ALIF_SEATS


def _is_ta_marbuta(char: str) -> bool:
    """Check if a character is ta marbuta (pure function)."""
    return char == _TA_MARBUTA


def parse_vocalized(text: str) -> ParseResult:
    """Parse a vocalized Arabic string into an ordered sequence of (letter, mark) pairs.

    This is a pure function. It does NOT:
    - Extract roots or weights
    - Classify words as noun/verb/particle
    - Determine tense or transitivity
    - Produce any morphological information

    It ONLY:
    - Identifies letters from the LetterRegistry
    - Identifies marks from the MarkRegistry
    - Pairs each letter with its following mark (if any)
    - Records residuals for unvocalized letters or special characters

    Parameters
    ----------
    text : str
        A vocalized Arabic string (e.g. "كَتَبَ").

    Returns
    -------
    ParseResult
        The parsed result with units and metadata.

    Raises
    ------
    ValueError
        With FailureCode if the text contains unrecognized characters.
    """
    if not text or not text.strip():
        raise ValueError(
            f"{FailureCode.M_00_06.value}: input text is empty"
        )

    units: list[ParsedUnit] = []
    i = 0
    has_unvocalized = False

    while i < len(text):
        char = text[i]

        # Skip whitespace
        if char.isspace():
            i += 1
            continue

        # Case 1: Arabic letter in the 28-letter registry
        if _is_arabic_letter(char):
            letter = LETTER_BY_GLYPH[char]
            raw_letter = char
            i += 1

            # Check if next character is a mark
            mark: Optional[MarkIdentity] = None
            raw_mark = ""
            if i < len(text) and _is_arabic_mark(text[i]):
                raw_mark = text[i]
                mark = MARK_BY_GLYPH[raw_mark]
                i += 1
                # Handle shadda + vowel combination (shadda then vowel)
                if mark.mark_id == "SHADDA" and i < len(text) and _is_arabic_mark(text[i]):
                    # Shadda is followed by another mark — we keep shadda as the mark
                    # and the follow-up vowel will be handled as part of the unit building
                    raw_mark += text[i]
                    i += 1

            residuals: FrozenSet[str] = frozenset()
            if mark is None:
                has_unvocalized = True
                residuals = frozenset({"missing_harakat"})

            units.append(ParsedUnit(
                letter=letter,
                mark=mark,
                is_alif_seat=False,
                raw_letter=raw_letter,
                raw_mark=raw_mark,
                residuals=residuals,
            ))

        # Case 2: Alif seat (not in the 28 letters)
        elif _is_alif_seat(char):
            raw_letter = char
            i += 1

            # Check for attached mark
            mark = None
            raw_mark = ""
            if i < len(text) and _is_arabic_mark(text[i]):
                raw_mark = text[i]
                mark = MARK_BY_GLYPH[raw_mark]
                i += 1

            residuals = frozenset({"alif_seat_requires_domain_license"})
            if char == _ALIF_HAMZA_BELOW:
                residuals = frozenset({"hamzat_wasl_requires_domain_license"})

            units.append(ParsedUnit(
                letter=None,
                mark=mark,
                is_alif_seat=True,
                raw_letter=raw_letter,
                raw_mark=raw_mark,
                residuals=residuals,
            ))

        # Case 3: Ta marbuta (special letter form)
        elif _is_ta_marbuta(char):
            raw_letter = char
            i += 1

            mark = None
            raw_mark = ""
            if i < len(text) and _is_arabic_mark(text[i]):
                raw_mark = text[i]
                mark = MARK_BY_GLYPH[raw_mark]
                i += 1

            units.append(ParsedUnit(
                letter=None,
                mark=mark,
                is_alif_seat=False,
                raw_letter=raw_letter,
                raw_mark=raw_mark,
                residuals=frozenset({"ta_marbuta_requires_word_layer"}),
            ))

        # Case 4: Unrecognized character
        else:
            # Check if it's a combining mark without a preceding letter
            if _is_arabic_mark(char):
                raise ValueError(
                    f"{FailureCode.M_00_03.value}: orphaned mark '{char}' "
                    f"(U+{ord(char):04X}) without preceding letter at position {i}"
                )
            raise ValueError(
                f"{FailureCode.M_00_03.value}: unrecognized character '{char}' "
                f"(U+{ord(char):04X}) at position {i}"
            )

    if not units:
        raise ValueError(
            f"{FailureCode.M_00_06.value}: no Arabic characters found in input"
        )

    is_fully_vocalized = not has_unvocalized
    result_residuals: FrozenSet[str] = frozenset()
    if not is_fully_vocalized:
        result_residuals = frozenset({"missing_harakat"})

    return ParseResult(
        units=tuple(units),
        is_fully_vocalized=is_fully_vocalized,
        residuals=result_residuals,
    )
