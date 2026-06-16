"""
Vowel — 4 short vowels + 3 madd (long vowels). Closed set.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 (Category 2: Vowel); docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-06
"""
from __future__ import annotations

from enum import Enum

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class Vowel(str, Enum):
    """Closed set of 7 vowel markers (4 short + 3 madd).

    Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Vowel)
    """

    # Short vowels
    FATHA = "fatha"   # short a  (َ)
    DAMMA = "damma"   # short u  (ُ)
    KASRA = "kasra"   # short i  (ِ)
    SUKUN = "sukun"   # no vowel (ْ)

    # Madd (long vowels)
    ALIF_MADD = "alif_madd"  # long a — mediated by alif (ا)
    WAW_MADD  = "waw_madd"   # long u — mediated by waw (و)
    YA_MADD   = "ya_madd"    # long i — mediated by ya  (ي)


SHORT_VOWELS: frozenset[Vowel] = frozenset(
    {Vowel.FATHA, Vowel.DAMMA, Vowel.KASRA, Vowel.SUKUN}
)

MADD_VOWELS: frozenset[Vowel] = frozenset(
    {Vowel.ALIF_MADD, Vowel.WAW_MADD, Vowel.YA_MADD}
)


def is_short(v: Vowel) -> bool:
    """Pure predicate: True iff ``v`` is a short vowel."""
    return v in SHORT_VOWELS


def is_madd(v: Vowel) -> bool:
    """Pure predicate: True iff ``v`` is a madd (long) vowel."""
    return v in MADD_VOWELS


def assert_valid_vowel(v: object) -> Vowel:
    """Assert ``v`` is a valid ``Vowel`` member.

    Raises
    ------
    ValueError
        With ``FailureCode.M_00_04`` if ``v`` is not a ``Vowel``.
    """
    if not isinstance(v, Vowel):
        raise ValueError(
            f"{FailureCode.M_00_04.value}: {v!r} is not a valid Vowel"
        )
    return v
