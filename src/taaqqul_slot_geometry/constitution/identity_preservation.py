"""
Identity Preservation — enforces Identity(source) ⊆ Identity(target).
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class IdentityLossError(ValueError):
    """Raised when Identity(source) ⊄ Identity(target).

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7
    """

    def __init__(self, lost: FrozenSet[str], failure_code: FailureCode) -> None:
        super().__init__(
            f"{failure_code.value}: identity attributes lost on transition: {lost}"
        )
        self.lost = lost
        self.failure_code = failure_code


@dataclass(frozen=True)
class IdentityPreservation:
    """Frozen record verifying that source identity is preserved in the target.

    Fields
    ------
    source_identity : FrozenSet[str]
        The set of identifying attributes of the source entity.
    added_attributes : FrozenSet[str]
        New attributes contributed by the target (may be empty).
    preserved : FrozenSet[str]
        The set of source attributes that ARE present in the target.
    trace_ref : str
        Reference to the constitutional clause authorising this check.
    rank : str
        Always ``"CANDIDATE"`` — may never be promoted in L0.
    residuals : FrozenSet[str]
        Any residual attributes not yet accounted for.
    """

    source_identity: FrozenSet[str]
    added_attributes: FrozenSet[str]
    preserved: FrozenSet[str]
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        # Birth guard — Rule 2: mandatory fields
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)

        # Identity preservation axiom
        lost = self.source_identity - self.preserved
        if lost:
            raise IdentityLossError(lost, FailureCode.M_CX_01)

    @property
    def target_identity(self) -> FrozenSet[str]:
        """Derived identity of the target (preserved ∪ added)."""
        return self.preserved | self.added_attributes
