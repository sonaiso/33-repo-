"""
LinguisticSignified and ConventionalSignified.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (LinguisticSignified, ConventionalSignified)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


@dataclass(frozen=True)
class LinguisticSignified:
    """The linguistic (intra-systemic) content of a sign.

    In L0 this is a placeholder — full semantic content requires L1 bridges.

    Parameters
    ----------
    concept_label : str
        A label for the concept (no real-world claim yet).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    concept_label: str
    trace_ref: str = (
        "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (LinguisticSignified)"
    )
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.concept_label:
            raise ValueError(FailureCode.M_00_20.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class ConventionalSignified:
    """The conventional (socially-established) content of a sign.

    Parameters
    ----------
    convention_label : str
        A label for the convention.
    linguistic_signified : LinguisticSignified
        The underlying linguistic signified.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    convention_label: str
    linguistic_signified: LinguisticSignified
    trace_ref: str = (
        "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (ConventionalSignified)"
    )
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.convention_label:
            raise ValueError(FailureCode.M_00_20.value)
        if self.linguistic_signified is None:
            raise ValueError(FailureCode.M_00_20.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
