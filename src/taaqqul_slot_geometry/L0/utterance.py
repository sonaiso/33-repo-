"""
Utterance — an ordered sequence of Syllables.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Utterance)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.syllable import Syllable


@dataclass(frozen=True)
class Utterance:
    """An ordered, non-empty sequence of ``Syllable`` objects.

    This is the phonological word-level unit.  It does NOT carry meaning —
    it is a licensed candidate only (Rule 10: no meaning from weight alone).

    Parameters
    ----------
    syllables : Tuple[Syllable, ...]
        Ordered sequence of syllables (must be non-empty).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    syllables: Tuple[Syllable, ...]
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Utterance)"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.syllables:
            raise ValueError(FailureCode.M_00_06.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)

    @property
    def syllable_count(self) -> int:
        return len(self.syllables)
