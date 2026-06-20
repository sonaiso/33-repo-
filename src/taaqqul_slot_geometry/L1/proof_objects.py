"""
L1 Proof Objects — proof-carrying constitutional stubs only.

Origin: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-33
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


Rank = Literal["CANDIDATE"]


@dataclass(frozen=True)
class ProofTrace:
    """Immutable proof trace envelope."""

    trace_id: str
    trace_ref: str
    steps: Tuple[str, ...]
    evidence_refs: Tuple[str, ...] = ()
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if not self.evidence_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)


@dataclass(frozen=True)
class ProofObject:
    """Base proof object for L1 contracts."""

    proof_id: str
    proof_kind: str
    domain_id: str
    checked_gate_ids: Tuple[str, ...]
    checked_bridge_ids: Tuple[str, ...]
    preserved_identity_refs: Tuple[str, ...]
    forbidden_outputs_checked: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    residual_codes: Tuple[str, ...]
    failure_codes: Tuple[str, ...]
    trace: ProofTrace
    trace_ref: str
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)
        if not self.proof_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.proof_kind:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.domain_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)


@dataclass(frozen=True)
class MRKProof(ProofObject):
    """MRK proof contract."""


@dataclass(frozen=True)
class DomainProof(ProofObject):
    """Domain proof contract."""

    domain_contract_ref: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.domain_contract_ref:
            raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class IdentityProof(ProofObject):
    """Identity-preservation proof contract."""

    source_identity_refs: Tuple[str, ...] = ()
    target_identity_refs: Tuple[str, ...] = ()
    lost_identity_refs: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.lost_identity_refs:
            raise ValueError(FailureCode.M_CX_01.value)


@dataclass(frozen=True)
class GateProof(ProofObject):
    """Gate proof contract."""

    gate_id: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.gate_id:
            raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class BridgeProof(ProofObject):
    """Bridge proof contract."""

    bridge_id: str = ""
    source_domain_id: str = ""
    target_domain_id: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.bridge_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.source_domain_id or not self.target_domain_id:
            raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class EvidenceProof(ProofObject):
    """Evidence proof contract."""

    evidence_scope: Tuple[str, ...] = ()
    invalidators_checked: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.evidence_scope:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.invalidators_checked:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.residual_codes and not self.residuals:
            raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class CoverageProof(ProofObject):
    """Coverage proof contract."""

    positive_case_ids: Tuple[str, ...] = ()
    negative_case_ids: Tuple[str, ...] = ()
    residual_case_ids: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.positive_case_ids:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.negative_case_ids:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.residual_case_ids:
            raise ValueError(FailureCode.M_00_22.value)


__all__ = [
    "BridgeProof",
    "CoverageProof",
    "DomainProof",
    "EvidenceProof",
    "GateProof",
    "IdentityProof",
    "MRKProof",
    "ProofObject",
    "ProofTrace",
    "Rank",
]
