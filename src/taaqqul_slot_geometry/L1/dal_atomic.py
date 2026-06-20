"""
L1 DAL Atomic contracts (D1_DAL_ONLY).

Origin: docs/10_DAL_ATOMIC_CONSTITUTION.md
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-35
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.domain_ids import DomainID

Rank = Literal["CANDIDATE"]

DAL_ONLY_FORBIDDEN_OUTPUTS: Tuple[str, ...] = (
    "ROOT_FORM",
    "PATTERN_FORM",
    "WORD_FORM",
    "TOOL_FORM",
    "MABNI_FORM",
    "LEXICAL_MEANING",
    "ISNAD",
    "IFADAH",
    "HUKM",
    "TANZIL",
)


def _validate_common(
    *,
    trace_ref: str,
    rank: str,
    forbidden_outputs: Tuple[str, ...],
    proof_object_ref: str,
    proof_trace_ref: str,
) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)
    if rank != "CANDIDATE":
        raise ValueError(FailureCode.M_01_16.value)
    if not forbidden_outputs:
        raise ValueError(FailureCode.M_00_22.value)
    if not proof_object_ref and not proof_trace_ref:
        raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class CarrierIdentitySlot:
    """DAL carrier identity slot contract."""

    slot_id: str
    carrier_symbol: str
    carrier_index: int
    edge_state_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_ONLY_FORBIDDEN_OUTPUTS
    trace_ref: str = "docs/10_DAL_ATOMIC_CONSTITUTION.md"
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.slot_id or not self.carrier_symbol:
            raise ValueError(FailureCode.M_00_22.value)
        if self.carrier_index < 0:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.edge_state_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain_id != DomainID.D1_DAL_ONLY:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class HarakaFunctionSlot:
    """DAL haraka function slot contract."""

    slot_id: str
    carrier_slot_ref: str
    haraka_mark: str
    incoming_edge_ref: str
    outgoing_edge_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_ONLY_FORBIDDEN_OUTPUTS
    trace_ref: str = "docs/10_DAL_ATOMIC_CONSTITUTION.md"
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.slot_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.carrier_slot_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.haraka_mark:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.incoming_edge_ref or not self.outgoing_edge_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain_id != DomainID.D1_DAL_ONLY:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class EdgeState:
    """DAL edge state contract between slots."""

    edge_id: str
    from_slot_ref: str
    to_slot_ref: str
    transition_label: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_ONLY_FORBIDDEN_OUTPUTS
    trace_ref: str = "docs/10_DAL_ATOMIC_CONSTITUTION.md"
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.edge_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.from_slot_ref or not self.to_slot_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.transition_label:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain_id != DomainID.D1_DAL_ONLY:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class ClosureCell:
    """DAL closure cell contract (carrier/haraka/edge closure)."""

    cell_id: str
    carrier_slot_refs: Tuple[str, ...]
    haraka_slot_refs: Tuple[str, ...]
    edge_state_refs: Tuple[str, ...]
    waqf_wasl_projection_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_ONLY_FORBIDDEN_OUTPUTS
    trace_ref: str = "docs/10_DAL_ATOMIC_CONSTITUTION.md"
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.cell_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.carrier_slot_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.haraka_slot_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.edge_state_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.waqf_wasl_projection_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain_id != DomainID.D1_DAL_ONLY:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class SurfaceSkeletonCandidate:
    """DAL surface skeleton contract (not a LAFZI form candidate)."""

    candidate_id: str
    closure_cell_ref: str
    carrier_slot_refs: Tuple[str, ...]
    haraka_slot_refs: Tuple[str, ...]
    waqf_wasl_projection_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_ONLY_FORBIDDEN_OUTPUTS
    trace_ref: str = "docs/10_DAL_ATOMIC_CONSTITUTION.md"
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.closure_cell_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.carrier_slot_refs or not self.haraka_slot_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.waqf_wasl_projection_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain_id != DomainID.D1_DAL_ONLY:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class BridgeRequiredMarker:
    """DAL marker enforcing DalToLafzi bridge before leaving DAL_ONLY."""

    marker_id: str
    source_domain_id: DomainID
    target_domain_id: DomainID
    required_bridge_id: str
    reason: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = DAL_ONLY_FORBIDDEN_OUTPUTS
    trace_ref: str = "docs/10_DAL_ATOMIC_CONSTITUTION.md"
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.marker_id:
            raise ValueError(FailureCode.M_00_22.value)
        if self.source_domain_id != DomainID.D1_DAL_ONLY:
            raise ValueError(FailureCode.M_00_22.value)
        if self.target_domain_id != DomainID.D2_LAFZI_FORM:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.required_bridge_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.reason:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


__all__ = [
    "BridgeRequiredMarker",
    "CarrierIdentitySlot",
    "ClosureCell",
    "DAL_ONLY_FORBIDDEN_OUTPUTS",
    "EdgeState",
    "HarakaFunctionSlot",
    "Rank",
    "SurfaceSkeletonCandidate",
]
