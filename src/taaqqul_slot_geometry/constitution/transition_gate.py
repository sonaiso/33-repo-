"""
TransitionGate — verifies adjacency and identity preservation for all layer transitions.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, FrozenSet, Protocol, runtime_checkable

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.constitution.identity_preservation import (
    IdentityLossError,
    IdentityPreservation,
)

# Layer indices (used for adjacency check)
LAYER_INDEX: dict[str, int] = {
    "L0": 0,
    "L1": 1,
    "L2": 2,
    "L3": 3,
}


class TransitionError(ValueError):
    """Raised by TransitionGate when a transition is constitutionally invalid.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 8
    """

    def __init__(self, message: str, failure_code: FailureCode) -> None:
        super().__init__(f"{failure_code.value}: {message}")
        self.failure_code = failure_code


@runtime_checkable
class LayerEntity(Protocol):
    """Protocol for any entity that can participate in a layer transition."""

    trace_ref: str
    rank: str
    residuals: FrozenSet[str]


@dataclass(frozen=True)
class TransitionGate:
    """Immutable gate that validates a transition between two layers.

    Constitution guarantees enforced:
      - No leap: ``abs(source_layer_idx - target_layer_idx) == 1``
      - Identity preservation: ``Identity(source) ⊆ Identity(target)``

    Parameters
    ----------
    source_layer : str
        One of ``"L0"``, ``"L1"``, ``"L2"``, ``"L3"``.
    target_layer : str
        One of ``"L0"``, ``"L1"``, ``"L2"``, ``"L3"``.
    bridge_license_ref : str
        Reference to the ``LicensedBridge`` authorising this crossing.
    trace_ref : str
        Reference to the constitutional clause.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    source_layer: str
    target_layer: str
    bridge_license_ref: str
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6,7,8"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise TransitionError("trace_ref is empty", FailureCode.M_CX_12)
        if self.rank != "CANDIDATE":
            raise TransitionError("rank above CANDIDATE", FailureCode.M_CX_09)
        if not self.bridge_license_ref:
            raise TransitionError(
                "bridge_license_ref is empty", FailureCode.M_CX_03
            )
        if self.source_layer not in LAYER_INDEX:
            raise TransitionError(
                f"unknown source layer: {self.source_layer}",
                FailureCode.M_CX_13,
            )
        if self.target_layer not in LAYER_INDEX:
            raise TransitionError(
                f"unknown target layer: {self.target_layer}",
                FailureCode.M_CX_13,
            )
        self._check_adjacency()

    def _check_adjacency(self) -> None:
        """Enforce No-Leap Axiom (Rule 8)."""
        src_idx = LAYER_INDEX[self.source_layer]
        tgt_idx = LAYER_INDEX[self.target_layer]
        if abs(src_idx - tgt_idx) != 1:
            raise TransitionError(
                f"leap from {self.source_layer} to {self.target_layer} is forbidden",
                FailureCode.M_CX_02,
            )

    def prove_transition(
        self,
        source_identity: FrozenSet[str],
        target_identity: FrozenSet[str],
        added_attributes: FrozenSet[str] | None = None,
    ) -> IdentityPreservation:
        """Verify identity preservation and return the proof record.

        Parameters
        ----------
        source_identity : FrozenSet[str]
            Identifying attributes of the source entity.
        target_identity : FrozenSet[str]
            Identifying attributes of the target entity (must contain source).
        added_attributes : FrozenSet[str] or None
            Attributes added by the target (optional).

        Returns
        -------
        IdentityPreservation
            Proof that identity was preserved.

        Raises
        ------
        IdentityLossError
            If ``source_identity ⊄ target_identity``.
        """
        if added_attributes is None:
            added_attributes = target_identity - source_identity
        preserved = source_identity & target_identity
        return IdentityPreservation(
            source_identity=source_identity,
            added_attributes=added_attributes,
            preserved=preserved,
            trace_ref=self.trace_ref,
            rank=self.rank,
            residuals=self.residuals,
        )
