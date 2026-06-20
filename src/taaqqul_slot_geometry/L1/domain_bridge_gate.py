"""
L1 domain operation, gate, and bridge specifications.

Origin: docs/06_DOMAIN_SLOT_GEOMETRY_CONSTITUTION.md Domain-SGE Structure
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-34
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.domain_ids import DomainID

Rank = Literal["CANDIDATE"]


@dataclass(frozen=True)
class OperationSpec:
    """Domain-scoped operation contract."""

    operation_id: str
    source_domain_id: DomainID
    target_domain_id: DomainID
    operation_kind: str
    input_contract_refs: Tuple[str, ...]
    output_contract_refs: Tuple[str, ...]
    forbidden_outputs: Tuple[str, ...]
    required_gate_ids: Tuple[str, ...]
    trace_ref: str
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.source_domain_id, DomainID):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.target_domain_id, DomainID):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.operation_kind:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.input_contract_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.output_contract_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.forbidden_outputs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.required_gate_ids:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)


@dataclass(frozen=True)
class GateSpec:
    """Executable gate contract reference."""

    gate_id: str
    source_domain_id: DomainID
    input_contract_ref: str
    predicate_ref: str
    failure_code: FailureCode
    residual_code: str
    forbidden_outputs: Tuple[str, ...]
    trace_ref: str
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.gate_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.source_domain_id, DomainID):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.input_contract_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.predicate_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.failure_code, FailureCode):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.residual_code:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.forbidden_outputs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)


@dataclass(frozen=True)
class BridgeSpec:
    """Cross-domain bridge contract reference."""

    bridge_id: str
    source_domain_id: DomainID
    target_domain_id: DomainID
    source_contract_ref: str
    target_contract_ref: str
    translator_ref: str
    invariant_policy_ref: str
    required_proof_kinds: Tuple[str, ...]
    forbidden_outputs: Tuple[str, ...]
    trace_ref: str
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.bridge_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.source_domain_id, DomainID):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.target_domain_id, DomainID):
            raise ValueError(FailureCode.M_00_22.value)
        if self.source_domain_id == self.target_domain_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.source_contract_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.target_contract_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.translator_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.invariant_policy_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.required_proof_kinds:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.forbidden_outputs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)


__all__ = [
    "BridgeSpec",
    "GateSpec",
    "OperationSpec",
    "Rank",
]
