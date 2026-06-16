"""
ResidualBundle — frozen set of unresolved attributes carried by every entity.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2 (residuals field)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


@dataclass(frozen=True)
class ResidualBundle:
    """Frozen container for residual attributes of a constitutional entity.

    Parameters
    ----------
    items : FrozenSet[str]
        The set of residual attribute names (may be empty).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Nested residuals (always empty for this record itself).
    """

    items: FrozenSet[str] = field(default_factory=frozenset)
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)

    def union(self, other: ResidualBundle) -> ResidualBundle:
        """Return a new bundle with the union of items from both bundles."""
        return ResidualBundle(
            items=self.items | other.items,
            trace_ref=self.trace_ref,
            rank=self.rank,
        )

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, item: object) -> bool:
        return item in self.items
