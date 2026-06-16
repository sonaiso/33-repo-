"""
TraceRef — reference system linking every entity to the constitution.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


@dataclass(frozen=True)
class TraceRef:
    """Immutable reference to a constitutional clause.

    Parameters
    ----------
    doc : str
        The document name, e.g. ``"docs/00_MAQOOL_CONSTITUTION.md"``.
    section : str
        The section identifier, e.g. ``"§3"``.
    clause : str
        Optional clause label, e.g. ``"MCE-1"``.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle (may be empty).
    """

    doc: str
    section: str
    clause: str = ""
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.doc:
            raise ValueError(FailureCode.M_CX_12.value)
        if not self.section:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)

    @property
    def ref(self) -> str:
        """Full reference string."""
        parts = [self.doc, self.section]
        if self.clause:
            parts.append(f"({self.clause})")
        return " ".join(parts)

    def __str__(self) -> str:
        return self.ref
