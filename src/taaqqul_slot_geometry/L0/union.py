"""
Union — the pairing of a Signifier with a ConventionalSignified to form a sign.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Union)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.signified import ConventionalSignified
from taaqqul_slot_geometry.L0.signifier import Signifier


@dataclass(frozen=True)
class Union:
    """The constitutional union of a signifier and a conventional signified.

    This is the minimal complete sign in L0.  It does NOT yet constitute
    full signification — that requires a ``Signification`` type assignment.

    Parameters
    ----------
    signifier : Signifier
        The phonological form.
    signified : ConventionalSignified
        The conventional content.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    signifier: Signifier
    signified: ConventionalSignified
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Union)"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.signifier is None:
            raise ValueError(FailureCode.M_00_19.value)
        if self.signified is None:
            raise ValueError(FailureCode.M_00_20.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
