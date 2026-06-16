"""
Signifier — a licensed Utterance that has been validated for phonological well-formedness.
Origin: docs/00_MAQOOL_CONSTITUTION.md §8 P1 (Sound Primacy); §2 Category 2 (Signifier)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.utterance import Utterance


@dataclass(frozen=True)
class Signifier:
    """A constitutionally-licensed utterance that may carry a signified.

    A ``Signifier`` MUST be grounded in an ``Utterance`` (Postulate P1).
    It does NOT yet carry meaning — that requires the ``Union`` in L0 and
    a licensed bridge to L1.

    Parameters
    ----------
    utterance : Utterance
        The phonological substrate.
    license_ref : str
        Reference to the licensing rule (e.g. ``"P1:sound_primacy"``).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    utterance: Utterance
    license_ref: str
    domain_tag: str = "L0_SIGNIFIER"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §8 P1"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.utterance is None:
            raise ValueError(FailureCode.M_00_18.value)
        if not self.license_ref:
            raise ValueError(FailureCode.M_00_18.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
