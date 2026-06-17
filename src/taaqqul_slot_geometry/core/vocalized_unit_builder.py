"""
VocalizedUnitBuilder — converts (letter, mark) pairs into PhonemeUnits.

Takes the output of VocalizedParser and produces PhonemeUnit objects
by applying the LETTER_HARAKA_LINK transition law.

This module operates ONLY at the L0 level:
- It maps letter+mark pairs to PhoneticPattern
- It validates that the transition is licensed (no preventers)
- It does NOT determine word class, root, or weight

Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedUnitBuilder
trace_ref: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedUnitBuilder
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Optional, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.letter_registry import LetterIdentity, LetterGenus
from taaqqul_slot_geometry.core.mark_registry import MarkIdentity, MarkFunction
from taaqqul_slot_geometry.core.transition_registry import (
    TransitionVerdict,
    check_transition_licensed,
)
from taaqqul_slot_geometry.core.vocalized_parser import ParsedUnit, ParseResult
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern


# ── Mark function to PhoneticPattern mapping ──────────────────────────────────

_MARK_TO_PATTERN: dict[str, PhoneticPattern] = {
    "FATHA": PhoneticPattern.C_FATHA,
    "DAMMA": PhoneticPattern.C_DAMMA,
    "KASRA": PhoneticPattern.C_KASRA,
    "SUKUN": PhoneticPattern.C_SUKUN,
    "FATHATAN": PhoneticPattern.C_FATHA,   # tanwin = short vowel + nunnation effect
    "DAMMATAN": PhoneticPattern.C_DAMMA,
    "KASRATAN": PhoneticPattern.C_KASRA,
}


@dataclass(frozen=True)
class VocalizedUnit:
    """A single vocalized unit: letter + pattern determined by its mark.

    This is the intermediate representation between parsed text and PhonemeUnit.

    Parameters
    ----------
    phoneme : PhonemeUnit
        The resulting phoneme unit.
    letter_glyph : str
        The raw letter glyph.
    mark_id : Optional[str]
        The mark ID applied (None if no mark is attached).
    transition_verdict : TransitionVerdict
        Whether this unit's formation was licensed.
    is_tanwin : bool
        Whether the mark is tanwin (has post-L0 effects).
    is_shadda : bool
        Whether shadda is present (gemination).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    phoneme: PhonemeUnit
    letter_glyph: str
    mark_id: Optional[str]
    transition_verdict: TransitionVerdict
    is_tanwin: bool = False
    is_shadda: bool = False
    trace_ref: str = "docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedUnitBuilder"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.letter_glyph:
            raise ValueError(
                f"{FailureCode.M_00_14.value}: letter_glyph cannot be empty"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


def _determine_pattern(
    letter: Optional[LetterIdentity],
    mark: Optional[MarkIdentity],
    is_alif_seat: bool,
    next_unit: Optional[ParsedUnit] = None,
) -> Tuple[PhoneticPattern, FrozenSet[str]]:
    """Determine the PhoneticPattern from a letter+mark pair (pure function).

    Returns
    -------
    Tuple[PhoneticPattern, FrozenSet[str]]
        The pattern and any residuals.
    """
    residuals: FrozenSet[str] = frozenset()

    # Alif seat cases: alif acts as madd carrier
    if is_alif_seat:
        # Alif with fatha before it = long vowel (CVV)
        return PhoneticPattern.C_FATHA_MADD, frozenset({"alif_seat_requires_domain_license"})

    if letter is None:
        return PhoneticPattern.C_FATHA, frozenset({"letter_identity_missing"})

    if mark is None:
        # No mark = potential sukun (consonant closure) or missing vocalization
        return PhoneticPattern.C_SUKUN, frozenset({"missing_harakat"})

    # Check for long vowel pattern: letter + short vowel + long vowel letter
    # e.g. تَا = ت + fatha + alif → CVV pattern
    # This is handled at a higher level (syllabifier), not here.

    # Map mark to pattern
    mark_id = mark.mark_id
    if mark_id in _MARK_TO_PATTERN:
        pattern = _MARK_TO_PATTERN[mark_id]
        # Check tanwin
        if mark_id in ("FATHATAN", "DAMMATAN", "KASRATAN"):
            residuals = frozenset({"tanwin_requires_word_layer"})
        return pattern, residuals

    # Shadda: gemination — the underlying vowel determines the pattern
    if mark_id == "SHADDA":
        # Shadda alone without a following vowel = pending
        return PhoneticPattern.C_FATHA, frozenset({"shadda_pending_vowel"})

    # Maddah on alif seat
    if mark_id == "MADDAH":
        return PhoneticPattern.C_FATHA_MADD, residuals

    # Superscript alif
    if mark_id == "SUPERSCRIPT_ALIF":
        return PhoneticPattern.C_FATHA_MADD, frozenset({"orthographic_variant_ambiguity"})

    # Fallback
    return PhoneticPattern.C_FATHA, frozenset({"unknown_mark_pattern"})


def _check_letter_haraka_transition(
    letter: Optional[LetterIdentity],
    mark: Optional[MarkIdentity],
) -> TransitionVerdict:
    """Check if the letter+mark transition is licensed (pure function)."""
    if letter is None:
        # Alif seat — transition is conditionally licensed
        return TransitionVerdict.LICENSED

    if mark is None:
        # No mark — could be sukun or missing vocalization
        return TransitionVerdict.DEFERRED

    # Check preventers
    preventer_active = False

    # Preventer: sukun blocks haraka
    if mark.function == MarkFunction.CLOSE_LETTER:
        # Sukun is valid — it's a LETTER_SUKUN_LINK, not LETTER_HARAKA_LINK
        law_id = "LETTER_SUKUN_LINK"
    elif mark.function == MarkFunction.GEMINATE:
        law_id = "LETTER_SHADDA_LINK"
        if not letter.accepts_shadda:
            preventer_active = True
    else:
        law_id = "LETTER_HARAKA_LINK"
        if not letter.accepts_haraka:
            preventer_active = True

    return check_transition_licensed(
        law_id=law_id,
        carrier_exists=True,
        domain_declared=True,
        identity_preserved=True,
        operator_licensed=True,
        condition_holds=True,
        cause_exists=True,
        preventer_active=preventer_active,
    )


def build_vocalized_units(parse_result: ParseResult) -> Tuple[VocalizedUnit, ...]:
    """Convert a ParseResult into a sequence of VocalizedUnits (pure function).

    This function:
    - Maps each (letter, mark) pair to a PhonemeUnit via PhoneticPattern
    - Validates transitions via the TransitionRegistry
    - Records residuals for special cases (tanwin, shadda, alif seats)

    It does NOT:
    - Extract roots or weights
    - Classify words
    - Determine morphological information

    Parameters
    ----------
    parse_result : ParseResult
        Output from parse_vocalized().

    Returns
    -------
    Tuple[VocalizedUnit, ...]
        The ordered sequence of vocalized units.
    """
    results: list[VocalizedUnit] = []

    for idx, unit in enumerate(parse_result.units):
        # Determine next unit for look-ahead (for long vowel detection)
        next_unit = parse_result.units[idx + 1] if idx + 1 < len(parse_result.units) else None

        # Determine pattern
        pattern, pattern_residuals = _determine_pattern(
            unit.letter, unit.mark, unit.is_alif_seat, next_unit
        )

        # Check transition
        verdict = _check_letter_haraka_transition(unit.letter, unit.mark)

        # Determine consonant character for PhonemeUnit
        if unit.letter is not None:
            consonant = unit.letter.glyph
        else:
            consonant = unit.raw_letter  # Alif seat or special

        # Build the PhonemeUnit
        phoneme = PhonemeUnit(
            consonant=consonant,
            pattern=pattern,
        )

        # Determine mark info
        mark_id = unit.mark.mark_id if unit.mark else None
        is_tanwin = mark_id in ("FATHATAN", "DAMMATAN", "KASRATAN") if mark_id else False
        is_shadda = mark_id == "SHADDA" if mark_id else False

        # Combine residuals
        all_residuals = pattern_residuals | unit.residuals

        results.append(VocalizedUnit(
            phoneme=phoneme,
            letter_glyph=unit.raw_letter,
            mark_id=mark_id,
            transition_verdict=verdict,
            is_tanwin=is_tanwin,
            is_shadda=is_shadda,
            residuals=all_residuals,
        ))

    return tuple(results)
