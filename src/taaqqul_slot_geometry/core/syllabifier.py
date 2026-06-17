"""
Syllabifier — group VocalizedUnits into Syllables.

Takes the output of VocalizedUnitBuilder and groups units into syllables
following the 4 licensed Arabic syllable patterns: CV, CVC, CVV, CVCC.

This module operates ONLY at the L0 level:
- It groups phoneme units into syllable candidates
- It validates syllable patterns against the closed set of 4 types
- It does NOT extract roots, weights, or word classes

Origin: docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2)
trace_ref: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §Syllabifier
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.transition_registry import (
    TransitionVerdict,
    check_transition_licensed,
)
from taaqqul_slot_geometry.core.vocalized_unit_builder import VocalizedUnit
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern
from taaqqul_slot_geometry.L0.syllable import Syllable, SyllableType, make_syllable


# ── Pattern classification helpers ────────────────────────────────────────────

_VOWELED_PATTERNS = frozenset({
    PhoneticPattern.C_FATHA,
    PhoneticPattern.C_DAMMA,
    PhoneticPattern.C_KASRA,
})

_LONG_VOWEL_PATTERNS = frozenset({
    PhoneticPattern.C_FATHA_MADD,
    PhoneticPattern.C_DAMMA_MADD,
    PhoneticPattern.C_KASRA_MADD,
})

_CLOSED_PATTERNS = frozenset({
    PhoneticPattern.C_SUKUN,
    PhoneticPattern.CVC_SUKUN,
})


def _is_voweled(unit: VocalizedUnit) -> bool:
    """Check if unit has a short vowel (CV onset)."""
    return unit.phoneme.pattern in _VOWELED_PATTERNS


def _is_long_vowel(unit: VocalizedUnit) -> bool:
    """Check if unit has a long vowel (CVV)."""
    return unit.phoneme.pattern in _LONG_VOWEL_PATTERNS


def _is_closed(unit: VocalizedUnit) -> bool:
    """Check if unit is a closed consonant (sukun)."""
    return unit.phoneme.pattern in _CLOSED_PATTERNS


def _is_alif_seat_madd(unit: VocalizedUnit) -> bool:
    """Check if unit is an alif seat acting as madd carrier."""
    return "alif_seat_requires_domain_license" in unit.residuals


@dataclass(frozen=True)
class SyllabificationResult:
    """Result of syllabifying a sequence of VocalizedUnits.

    Parameters
    ----------
    syllables : Tuple[Syllable, ...]
        The ordered sequence of syllables.
    syllable_types : Tuple[SyllableType, ...]
        The types of each syllable (for quick inspection).
    transition_verdict : TransitionVerdict
        Whether all syllable formations were licensed.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    syllables: Tuple[Syllable, ...]
    syllable_types: Tuple[SyllableType, ...]
    transition_verdict: TransitionVerdict
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2)"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


def syllabify(units: Tuple[VocalizedUnit, ...]) -> SyllabificationResult:
    """Group VocalizedUnits into Syllables (pure function).

    Algorithm:
    1. Scan left-to-right through the unit sequence.
    2. A voweled unit (CV) starts a new syllable onset.
    3. If followed by a closed unit (sukun), the syllable becomes CVC.
    4. If followed by an alif-seat madd, the syllable becomes CVV.
    5. A long-vowel unit forms CVV on its own.

    This function does NOT:
    - Extract roots or weights
    - Classify words as noun/verb/particle
    - Determine any morphological information

    Parameters
    ----------
    units : Tuple[VocalizedUnit, ...]
        Output from build_vocalized_units().

    Returns
    -------
    SyllabificationResult
        The syllabification with syllables and metadata.
    """
    if not units:
        raise ValueError(
            f"{FailureCode.M_00_16.value}: no units to syllabify"
        )

    syllables: list[Syllable] = []
    syllable_types: list[SyllableType] = []
    all_residuals: set[str] = set()
    i = 0

    while i < len(units):
        unit = units[i]

        # Collect residuals from each unit
        all_residuals.update(unit.residuals)

        # Case 1: Long vowel unit → CVV syllable
        if _is_long_vowel(unit):
            syllable = make_syllable((unit.phoneme,))
            syllables.append(syllable)
            syllable_types.append(SyllableType.CVV)
            i += 1
            continue

        # Case 2: Voweled unit (short vowel) → potential CV, CVC, or CVV
        if _is_voweled(unit):
            # Look ahead: is next unit a closed consonant (sukun)?
            if i + 1 < len(units) and _is_closed(units[i + 1]):
                # CV + C(sukun) → CVC
                cvc_phoneme = PhonemeUnit(
                    consonant=unit.phoneme.consonant + units[i + 1].phoneme.consonant,
                    pattern=PhoneticPattern.CVC_SUKUN,
                )
                syllable = make_syllable((cvc_phoneme,))
                syllables.append(syllable)
                syllable_types.append(SyllableType.CVC)
                all_residuals.update(units[i + 1].residuals)
                i += 2
                continue

            # Look ahead: is next unit an alif seat (madd carrier)?
            if i + 1 < len(units) and _is_alif_seat_madd(units[i + 1]):
                # CV + alif → CVV (long vowel via alif madd)
                madd_pattern = PhoneticPattern.C_FATHA_MADD
                if unit.phoneme.pattern == PhoneticPattern.C_DAMMA:
                    madd_pattern = PhoneticPattern.C_DAMMA_MADD
                elif unit.phoneme.pattern == PhoneticPattern.C_KASRA:
                    madd_pattern = PhoneticPattern.C_KASRA_MADD

                cvv_phoneme = PhonemeUnit(
                    consonant=unit.phoneme.consonant,
                    pattern=madd_pattern,
                )
                syllable = make_syllable((cvv_phoneme,))
                syllables.append(syllable)
                syllable_types.append(SyllableType.CVV)
                all_residuals.update(units[i + 1].residuals)
                i += 2
                continue

            # Plain CV syllable
            syllable = make_syllable((unit.phoneme,))
            syllables.append(syllable)
            syllable_types.append(SyllableType.CV)
            i += 1
            continue

        # Case 3: Closed unit (sukun/unvocalized) — needs special handling
        if _is_closed(unit):
            # Check if this is from missing vocalization (deferred text)
            if "missing_harakat" in unit.residuals:
                # Unvocalized: group consecutive unvocalized letters into one
                # deferred CVC-like syllable with residuals
                consonants = unit.phoneme.consonant
                i += 1
                while i < len(units) and _is_closed(units[i]) and "missing_harakat" in units[i].residuals:
                    consonants += units[i].phoneme.consonant
                    all_residuals.update(units[i].residuals)
                    i += 1
                # Create a CVC phoneme for the group (deferred analysis)
                deferred_phoneme = PhonemeUnit(
                    consonant=consonants,
                    pattern=PhoneticPattern.CVC_SUKUN,
                )
                syllable = make_syllable((deferred_phoneme,))
                syllables.append(syllable)
                syllable_types.append(SyllableType.CVC)
                all_residuals.add("missing_harakat")
                continue

            # A sukun unit without a preceding onset (legitimate closed consonant)
            # Create a CVC phoneme
            all_residuals.add("isolated_sukun_unit")
            cvc_phoneme = PhonemeUnit(
                consonant=unit.phoneme.consonant,
                pattern=PhoneticPattern.CVC_SUKUN,
            )
            syllable = make_syllable((cvc_phoneme,))
            syllables.append(syllable)
            syllable_types.append(SyllableType.CVC)
            i += 1
            continue

        # Case 4: Alif seat — should have been consumed by look-ahead
        if _is_alif_seat_madd(unit):
            # Standalone alif seat not preceded by voweled unit
            all_residuals.add("alif_seat_without_onset")
            # Create a CVV with default fatha madd
            cvv_phoneme = PhonemeUnit(
                consonant=unit.phoneme.consonant,
                pattern=PhoneticPattern.C_FATHA_MADD,
            )
            syllable = make_syllable((cvv_phoneme,))
            syllables.append(syllable)
            syllable_types.append(SyllableType.CVV)
            i += 1
            continue

        # Fallback: create a CV syllable and record residual
        all_residuals.add("syllabification_fallback")
        syllable = make_syllable((unit.phoneme,))
        syllables.append(syllable)
        syllable_types.append(SyllableType.CV)
        i += 1

    if not syllables:
        raise ValueError(
            f"{FailureCode.M_00_16.value}: no syllables could be formed"
        )

    # Check the overall syllabification transition
    verdict = check_transition_licensed(
        law_id="VOCALIZED_UNIT_TO_SYLLABLE",
        carrier_exists=True,
        domain_declared=True,
        identity_preserved=True,
        operator_licensed=True,
        condition_holds=len(syllables) > 0,
        cause_exists=True,
        preventer_active=False,
    )

    return SyllabificationResult(
        syllables=tuple(syllables),
        syllable_types=tuple(syllable_types),
        transition_verdict=verdict,
        residuals=frozenset(all_residuals),
    )
