"""
Syllable — 4 closed syllable types composed of PhonemeUnits.
Origin: docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2); docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-04
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern


class SyllableType(str, Enum):
    """Closed set of exactly 4 syllable types (MCE-2).

    Origin: docs/00_MAQOOL_CONSTITUTION.md §4
    """

    CV   = "CV"    # consonant + short vowel
    CVC  = "CVC"   # consonant + vowel + consonant
    CVV  = "CVV"   # consonant + long vowel (madd)
    CVCC = "CVCC"  # consonant + vowel + consonant + consonant (closed heavy)


# Phonetic pattern sets associated with each syllable type
_CV_PATTERNS: FrozenSet[PhoneticPattern] = frozenset(
    {PhoneticPattern.C_FATHA, PhoneticPattern.C_DAMMA, PhoneticPattern.C_KASRA}
)
_CVC_PATTERNS: FrozenSet[PhoneticPattern] = frozenset(
    {PhoneticPattern.CVC_SUKUN}
)
_CVV_PATTERNS: FrozenSet[PhoneticPattern] = frozenset(
    {
        PhoneticPattern.C_FATHA_MADD,
        PhoneticPattern.C_DAMMA_MADD,
        PhoneticPattern.C_KASRA_MADD,
    }
)
# CVCC is represented as a sequence of two CVC∅ units (rare in Arabic)
_CVCC_PATTERNS: FrozenSet[PhoneticPattern] = frozenset(
    {PhoneticPattern.CVC_SUKUN}
)


def _infer_syllable_type(phonemes: Tuple[PhonemeUnit, ...]) -> SyllableType:
    """Infer the syllable type from a sequence of phoneme units (pure function).

    Rules
    -----
    - 1 phoneme with Ca/Cu/Ci pattern → CV
    - 1 phoneme with Caa/Cuu/Cii pattern → CVV
    - 1 phoneme with CVC∅ pattern → CVC
    - 2 phonemes both CVC∅ → CVCC

    Raises
    ------
    ValueError
        With ``FailureCode.M_00_17`` if the pattern cannot be matched to a type.
    """
    if len(phonemes) == 1:
        p = phonemes[0].pattern
        if p in _CV_PATTERNS:
            return SyllableType.CV
        if p in _CVV_PATTERNS:
            return SyllableType.CVV
        if p in _CVC_PATTERNS:
            return SyllableType.CVC
    if len(phonemes) == 2:
        if all(u.pattern in _CVCC_PATTERNS for u in phonemes):
            return SyllableType.CVCC
    raise ValueError(
        f"{FailureCode.M_00_17.value}: cannot infer syllable type from patterns "
        f"{[u.pattern.value for u in phonemes]}"
    )


@dataclass(frozen=True)
class Syllable:
    """A single syllable: an ordered sequence of ``PhonemeUnit``s.

    The ``syllable_type`` is derived automatically from the phoneme patterns
    if not supplied, and then validated.

    Parameters
    ----------
    phonemes : Tuple[PhonemeUnit, ...]
        The ordered phoneme units composing this syllable (1 or 2 units).
    syllable_type : SyllableType
        The type inferred or provided.  Must match the phoneme patterns.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    phonemes: Tuple[PhonemeUnit, ...]
    syllable_type: SyllableType
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2)"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.phonemes:
            raise ValueError(FailureCode.M_00_16.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        # Validate that the declared type matches the inferred type
        inferred = _infer_syllable_type(self.phonemes)
        if inferred != self.syllable_type:
            raise ValueError(
                f"{FailureCode.M_00_17.value}: declared type {self.syllable_type.value!r} "
                f"does not match inferred type {inferred.value!r}"
            )


def make_syllable(phonemes: Tuple[PhonemeUnit, ...]) -> Syllable:
    """Pure factory: infer type and construct a ``Syllable``.

    Raises
    ------
    ValueError
        With ``FailureCode.M_00_17`` if the phoneme sequence is invalid.
    """
    stype = _infer_syllable_type(phonemes)
    return Syllable(phonemes=phonemes, syllable_type=stype)
