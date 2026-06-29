"""
Aqd audit-only L1 contracts.

Origin: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
Authority: docs/00_MAQOOL_CONSTITUTION.md §5; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode

AqdRank = Literal["CANDIDATE"]
AqdAuditStatus = Literal[
    "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
    "AUDIT_SHAPE_INVALID_RUNTIME_STILL_BLOCKED",
    "AUDIT_REVERSE_REQUIRED_RUNTIME_STILL_BLOCKED",
]

AQD_TRACE_REF = "docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md"
AQD_FORBIDDEN_OUTPUTS: Tuple[str, ...] = (
    "RUNTIME_RESULT",
    "AUTHORITATIVE_DECISION",
    "FINAL_MEANING",
    "RELATION_RUNTIME",
    "IFADAH_RUNTIME",
    "HUKM",
    "TANZIL",
    "YAQIN",
    "KERNEL_DECISION",
)
_AQD_ALLOWED_STATUSES = frozenset(
    {
        "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
        "AUDIT_SHAPE_INVALID_RUNTIME_STILL_BLOCKED",
        "AUDIT_REVERSE_REQUIRED_RUNTIME_STILL_BLOCKED",
    }
)


def _require_non_empty(value: str) -> None:
    if not value:
        raise ValueError(FailureCode.M_00_22.value)


def _require_non_empty_refs(*refs: str) -> None:
    if not all(refs):
        raise ValueError(FailureCode.M_00_22.value)


def _require_trace_ref(trace_ref: str) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)


def _require_candidate_rank(rank: str) -> None:
    if rank != "CANDIDATE":
        raise ValueError(FailureCode.M_01_16.value)


def _require_proof_reference(proof_object_ref: str, proof_trace_ref: str) -> None:
    if not proof_object_ref and not proof_trace_ref:
        raise ValueError(FailureCode.M_00_22.value)


def _require_forbidden_outputs(forbidden_outputs: Tuple[str, ...]) -> None:
    if not forbidden_outputs:
        raise ValueError(FailureCode.M_00_22.value)
    if set(forbidden_outputs) != set(AQD_FORBIDDEN_OUTPUTS):
        raise ValueError(FailureCode.M_00_22.value)


def _require_audit_only_flags(authoritative: bool, runtime_authorized: bool) -> None:
    if authoritative is not False:
        raise ValueError(FailureCode.M_CX_02.value)
    if runtime_authorized is not False:
        raise ValueError(FailureCode.M_CX_02.value)


def _validate_contract_envelope(
    *,
    trace_ref: str,
    rank: str,
    proof_object_ref: str,
    proof_trace_ref: str,
    forbidden_outputs: Tuple[str, ...],
    authoritative: bool,
    runtime_authorized: bool,
) -> None:
    _require_trace_ref(trace_ref)
    _require_candidate_rank(rank)
    _require_proof_reference(proof_object_ref, proof_trace_ref)
    _require_forbidden_outputs(forbidden_outputs)
    _require_audit_only_flags(authoritative, runtime_authorized)


@dataclass(frozen=True)
class AqdUniversalContract:
    """Universal Aqd proof-bearing shape; not execution authority.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    universal_scope_ref: str
    obligation_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.universal_scope_ref,
            self.obligation_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdPartialBranchContract:
    """Partial branch contract with origin, relation triplet, and barrier refs.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    origin_ref: str
    branch_ref: str
    relation_with_prev_ref: str
    relation_with_next_ref: str
    relation_next_to_prev_ref: str
    condition_ref: str
    sabab_ref: str
    preventer_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.origin_ref,
            self.branch_ref,
            self.relation_with_prev_ref,
            self.relation_with_next_ref,
            self.relation_next_to_prev_ref,
            self.condition_ref,
            self.sabab_ref,
            self.preventer_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdAttributeContract:
    """Attribute contract; it does not attach final meaning to reality.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    carrier_ref: str
    attribute_ref: str
    relation_effect_candidate_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.carrier_ref,
            self.attribute_ref,
            self.relation_effect_candidate_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdRelationTripletContract:
    """Relation-function candidate triplet; not final relation authority.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    previous_relation_ref: str
    next_relation_ref: str
    next_to_previous_relation_ref: str
    relation_function_candidate_ref: str
    tool_surface_ref: str
    license_condition_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.previous_relation_ref,
            self.next_relation_ref,
            self.next_to_previous_relation_ref,
            self.relation_function_candidate_ref,
            self.tool_surface_ref,
            self.license_condition_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdTemporalBindingContract:
    """Temporal binding shape for audit; no time execution is performed.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    temporal_scope_ref: str
    utterance_time_ref: str
    attribute_time_ref: str
    temporal_policy_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.temporal_scope_ref,
            self.utterance_time_ref,
            self.attribute_time_ref,
            self.temporal_policy_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdInflectionAuditContract:
    """Inflection audit shape as licensed effect candidate only.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    operator_ref: str
    carrier_ref: str
    temporal_binding_ref: str
    effect_candidate_ref: str
    inflection_policy_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.operator_ref,
            self.carrier_ref,
            self.temporal_binding_ref,
            self.effect_candidate_ref,
            self.inflection_policy_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdMorphologicalBranchContract:
    """Morphological branch shape; surface weight alone licenses nothing.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    surface_weight_ref: str
    licensed_origin_ref: str
    branch_ref: str
    path_card_ref: str
    masdar_open_ref: str
    residual_policy_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.surface_weight_ref,
            self.licensed_origin_ref,
            self.branch_ref,
            self.path_card_ref,
            self.masdar_open_ref,
            self.residual_policy_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdReverseAuditContract:
    """Reverse audit shape; it records required refs without reverse execution.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    contract_id: str
    source_stage_ref: str
    target_stage_ref: str
    reverse_policy_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    forbidden_outputs: Tuple[str, ...] = AQD_FORBIDDEN_OUTPUTS
    authoritative: bool = False
    runtime_authorized: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty_refs(
            self.contract_id,
            self.source_stage_ref,
            self.target_stage_ref,
            self.reverse_policy_ref,
        )
        _validate_contract_envelope(**_contract_envelope_payload(self))


@dataclass(frozen=True)
class AqdAuditResult:
    """Shape audit result; runtime remains blocked even when shape is valid.

    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    shape_valid: bool
    status: AqdAuditStatus
    runtime_authorized: bool = False
    authoritative: bool = False
    trace_ref: str = AQD_TRACE_REF
    rank: AqdRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.shape_valid, bool):
            raise ValueError(FailureCode.M_00_22.value)
        if self.status not in _AQD_ALLOWED_STATUSES:
            raise ValueError(FailureCode.M_CX_02.value)
        _require_audit_only_flags(self.authoritative, self.runtime_authorized)
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)


def audit_aqd_contract_shape(contract: object) -> AqdAuditResult:
    """Return an audit-only shape result without runtime authority.

    contract: accepted Aqd audit contract instance.
    returns: AqdAuditResult with runtime_authorized always False.
    trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
    """

    if not isinstance(contract, _AQD_CONTRACT_TYPES):
        return AqdAuditResult(
            shape_valid=False,
            status="AUDIT_SHAPE_INVALID_RUNTIME_STILL_BLOCKED",
            residuals=frozenset({"AQD_CONTRACT_SHAPE_INVALID"}),
        )
    return AqdAuditResult(
        shape_valid=True,
        status="AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
        trace_ref=contract.trace_ref,
        residuals=contract.residuals,
    )


def _contract_envelope_payload(contract: object) -> dict:
    return {
        "trace_ref": getattr(contract, "trace_ref"),
        "rank": getattr(contract, "rank"),
        "proof_object_ref": getattr(contract, "proof_object_ref"),
        "proof_trace_ref": getattr(contract, "proof_trace_ref"),
        "forbidden_outputs": getattr(contract, "forbidden_outputs"),
        "authoritative": getattr(contract, "authoritative"),
        "runtime_authorized": getattr(contract, "runtime_authorized"),
    }


_AQD_CONTRACT_TYPES = (
    AqdUniversalContract,
    AqdPartialBranchContract,
    AqdAttributeContract,
    AqdRelationTripletContract,
    AqdTemporalBindingContract,
    AqdInflectionAuditContract,
    AqdMorphologicalBranchContract,
    AqdReverseAuditContract,
)

__all__ = [
    "AQD_FORBIDDEN_OUTPUTS",
    "AQD_TRACE_REF",
    "AqdAttributeContract",
    "AqdAuditResult",
    "AqdAuditStatus",
    "AqdInflectionAuditContract",
    "AqdMorphologicalBranchContract",
    "AqdPartialBranchContract",
    "AqdRank",
    "AqdRelationTripletContract",
    "AqdReverseAuditContract",
    "AqdTemporalBindingContract",
    "AqdUniversalContract",
    "audit_aqd_contract_shape",
]
