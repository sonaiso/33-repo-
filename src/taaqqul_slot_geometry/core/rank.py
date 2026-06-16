"""
Rank — ceiling lattice with CANDIDATE as the only permitted rank in L0.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2; §2 Category 1 (Rank, Candidate)
"""
from __future__ import annotations

from enum import Enum

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class Rank(str, Enum):
    """Rank lattice.

    In Phase 0 (L0), only ``CANDIDATE`` is permitted.  Higher ranks are
    reserved for future layers but may NEVER be assigned in L0.
    """

    CANDIDATE = "CANDIDATE"


class RankLattice:
    """Pure-function utilities for the rank lattice.

    All methods are static / class-level so no mutable state is created.
    """

    CEILING: Rank = Rank.CANDIDATE

    @classmethod
    def meet(cls, a: Rank, b: Rank) -> Rank:
        """Return the meet (greatest lower bound) of two ranks.

        Because ``CANDIDATE`` is the only member in Phase 0, the meet is
        always ``CANDIDATE``.  Any value above the ceiling raises an error.

        Raises
        ------
        ValueError
            With ``FailureCode.M_CX_09`` if a rank above the ceiling is given.
        """
        if a != cls.CEILING or b != cls.CEILING:
            raise ValueError(FailureCode.M_CX_09.value)
        return cls.CEILING

    @classmethod
    def assert_candidate(cls, rank: Rank) -> None:
        """Assert that ``rank`` is ``CANDIDATE`` (the only valid rank in L0).

        Raises
        ------
        ValueError
            With ``FailureCode.M_00_10`` if rank is above ceiling.
        """
        if rank != cls.CEILING:
            raise ValueError(
                f"{FailureCode.M_00_10.value}: rank {rank!r} is above CANDIDATE ceiling"
            )
