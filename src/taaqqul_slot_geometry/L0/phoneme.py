"""
PhoneticPattern (8 closed patterns) and PhonemeUnit.
Origin: docs/00_MAQOOL_CONSTITUTION.md §3 (MCE-1); docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-02
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class PhoneticPattern(str, Enum):
    """Closed set of exactly 8 phonetic patterns.

    No 9th pattern may be added (MCE-1).

    Origin: docs/00_MAQOOL_CONSTITUTION.md §3
    """

    C_FATHA = "Ca"       # consonant + fatha (short a)
    C_DAMMA = "Cu"       # consonant + damma (short u)
    C_KASRA = "Ci"       # consonant + kasra (short i)
    C_SUKUN = "C∅"       # consonant + sukun (no vowel)
    C_FATHA_MADD = "Caa" # consonant + alif madd (long a)
    C_DAMMA_MADD = "Cuu" # consonant + waw madd (long u)
    C_KASRA_MADD = "Cii" # consonant + ya madd (long i)
    CVC_SUKUN = "CVC∅"   # consonant + vowel + consonant + sukun


def _VALID_PATTERNS() -> FrozenSet[str]:
    return frozenset(p.value for p in PhoneticPattern)


@dataclass(frozen=True)
class PhonemeUnit:
    """A single phoneme: one consonant carrier bound to one phonetic pattern.

    Birth guards enforce:
      - ``consonant`` is a non-empty single character.
      - ``pattern`` is one of the 8 valid ``PhoneticPattern`` values.

    Parameters
    ----------
    consonant : str
        Single Arabic consonant character (or romanisation symbol).
    pattern : PhoneticPattern
        One of the 8 closed phonetic patterns.
    trace_ref : str
        Reference to the constitutional clause (§3, MCE-1).
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    consonant: str
    pattern: PhoneticPattern
    domain_tag: str = "L0_PHONETICS"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §3 (MCE-1)"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.consonant:
            raise ValueError(FailureCode.M_00_14.value)
        if len(self.consonant) > 4:
            raise ValueError(FailureCode.M_00_15.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        # pattern type check (also catches str passed as pattern)
        if not isinstance(self.pattern, PhoneticPattern):
            valid = ", ".join(p.value for p in PhoneticPattern)
            raise ValueError(
                f"{FailureCode.M_00_02.value}: pattern must be one of: {valid}"
            )
