"""
Weight patterns — 8 augmented forms + root weight.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10 (no meaning from weight alone)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class WeightPattern(str, Enum):
    """Augmented weight patterns for Arabic morphophonology.

    These patterns describe the phonological weight of a word form.
    They do NOT produce meaning (Rule 10).

    Pattern notation: C = consonant, V = short vowel, Vc = long vowel, 0 = silent.
    """

    ROOT         = "root"         # bare root consonants (no pattern applied)
    FAALA        = "faala"        # فَعَلَ  — basic trilateral active
    FAAL         = "faal"         # فَعْل   — masdar pattern 1
    FIAAL        = "fiaal"        # فِعَال  — masdar / broken plural
    FUAL         = "fual"         # فُعَال  — masdar / broken plural 2
    FAALIL       = "faalil"       # فَاعِل  — active participle
    MAFUUL       = "mafuul"       # مَفْعُول — passive participle
    TAFAALA      = "tafaala"      # تَفَاعَلَ — Form VI
    ISTAFALA     = "istafala"     # اسْتَفْعَلَ — Form X


@dataclass(frozen=True)
class WeightUnit:
    """A constitutionally-licensed weight assignment.

    This is a licensed CANDIDATE — it produces no meaning by itself.

    Parameters
    ----------
    pattern : WeightPattern
        The weight pattern applied.
    root_consonants : str
        The consonant skeleton (e.g. ``"ktb"``).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    pattern: WeightPattern
    root_consonants: str
    domain_tag: str = "L0_WEIGHT"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.pattern, WeightPattern):
            valid = ", ".join(p.value for p in WeightPattern)
            raise ValueError(
                f"{FailureCode.M_00_22.value}: pattern must be one of: {valid}"
            )
        if not self.root_consonants:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
