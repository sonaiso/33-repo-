"""
SlotGraph — the 9-tuple at the heart of the slot geometry.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 1 (SlotGraph, Center, Slots, Edges,
        Boundaries, Operations, Rank, Residuals, Trace)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank import Rank, RankLattice
from taaqqul_slot_geometry.core.residual import ResidualBundle
from taaqqul_slot_geometry.core.trace import TraceRef


@dataclass(frozen=True)
class SlotGraph:
    """The 9-tuple constitutional data structure.

    Tuple members (in order):
      1. center        — the focal entity
      2. slots         — ordered tuple of slot names
      3. edges         — frozen set of (slot_a, slot_b) pairs
      4. boundaries    — frozen set of boundary constraints
      5. operations    — frozen set of permitted operation names
      6. rank          — must be ``Rank.CANDIDATE`` in L0
      7. residuals     — residual bundle
      8. trace         — trace reference
      9. gamma         — gamma factor (layer context identifier, e.g. ``"L0"``)

    Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 1
    """

    center: Any
    slots: Tuple[str, ...]
    edges: FrozenSet[Tuple[str, str]]
    boundaries: FrozenSet[str]
    operations: FrozenSet[str]
    rank: Rank
    residuals: ResidualBundle
    trace: TraceRef
    gamma: str  # e.g. "L0", "L1", ...

    def __post_init__(self) -> None:
        # Birth guards
        if not self.trace.ref:
            raise ValueError(FailureCode.M_00_11.value)
        RankLattice.assert_candidate(self.rank)
        if not self.gamma:
            raise ValueError(FailureCode.M_CX_13.value)
