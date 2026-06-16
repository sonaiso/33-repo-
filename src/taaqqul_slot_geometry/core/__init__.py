"""
Core package — SlotGraph, Rank, ResidualBundle, TraceRef.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 1
"""
from taaqqul_slot_geometry.core.rank import Rank, RankLattice
from taaqqul_slot_geometry.core.residual import ResidualBundle
from taaqqul_slot_geometry.core.slot_graph import SlotGraph
from taaqqul_slot_geometry.core.trace import TraceRef

__all__ = [
    "Rank",
    "RankLattice",
    "ResidualBundle",
    "SlotGraph",
    "TraceRef",
]
