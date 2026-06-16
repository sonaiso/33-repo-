"""
Signification — types of signification relations (kuliyy, juz'iyy, mutabaqa, tadmin, iltizam).
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Signification)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.union import Union


class SignificationType(str, Enum):
    """Five types of signification recognised in the constitution.

    - KULLIYY    — universal/total signification
    - JUZIYY     — partial signification
    - MUTABAQA   — congruent (exact match) signification
    - TADMIN     — implicative / containment signification
    - ILTIZAM    — entailment / binding signification
    """

    KULLIYY  = "kulliyy"
    JUZIYY   = "juziyy"
    MUTABAQA = "mutabaqa"
    TADMIN   = "tadmin"
    ILTIZAM  = "iltizam"


@dataclass(frozen=True)
class Signification:
    """A constitutionally-typed signification relation.

    Parameters
    ----------
    sign : Union
        The sign being signified (signifier + signified).
    signification_type : SignificationType
        One of the 5 permitted types.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    sign: Union
    signification_type: SignificationType
    domain_tag: str = "L0_DALALAH"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Signification)"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.sign is None:
            raise ValueError(FailureCode.M_00_21.value)
        if not isinstance(self.signification_type, SignificationType):
            valid = ", ".join(s.value for s in SignificationType)
            raise ValueError(
                f"{FailureCode.M_00_21.value}: signification_type must be one of: {valid}"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
