"""
Euclidean learning contracts and gate-driven learning flow.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 1, 5, 7, 8
trace_ref: docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, Optional, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.transition_registry import EuclideanTransitionContract as RegistryTransitionContract


class ExecutionRank(str, Enum):
    """Execution rank for Euclidean gate outcomes."""

    ZERO = "ZERO"
    CANDIDATE = "CANDIDATE"
    HYPOTHESIS = "HYPOTHESIS"
    DEFERRED = "DEFERRED"
    LICENSED = "LICENSED"
    CERTIFIED = "CERTIFIED"
    BLOCKED = "BLOCKED"


_RANK_ORDER: Tuple[ExecutionRank, ...] = (
    ExecutionRank.ZERO,
    ExecutionRank.CANDIDATE,
    ExecutionRank.HYPOTHESIS,
    ExecutionRank.DEFERRED,
    ExecutionRank.LICENSED,
    ExecutionRank.CERTIFIED,
    ExecutionRank.BLOCKED,
)


class ResidualKind(str, Enum):
    """Residual impact levels used by Euclidean gate decisions."""

    NON_BLOCKING = "NON_BLOCKING"
    DEFERRED = "DEFERRED"
    BLOCKING = "BLOCKING"


@dataclass(frozen=True)
class Residual:
    """Classified residual attached to transition and gate outcomes."""

    code: str
    kind: ResidualKind
    message: str
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.code:
            raise ValueError(f"{FailureCode.M_CX_02.value}: residual code cannot be empty")
        if not self.message:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: residual message cannot be empty"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class Evidence:
    """Evidence supporting an origin→branch transition."""

    source: str
    claim: str
    evidence_rank: ExecutionRank
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError(f"{FailureCode.M_CX_02.value}: source cannot be empty")
        if not self.claim:
            raise ValueError(f"{FailureCode.M_CX_02.value}: claim cannot be empty")
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class MinimalCompleteRequirement:
    """Minimum required transition payload without layer overreach."""

    required_fields: Tuple[str, ...]
    forbidden_overreach: FrozenSet[str]
    max_rank: ExecutionRank
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.required_fields:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: required_fields cannot be empty"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class EuclideanTransitionContract:
    """Complete transition contract for Euclidean learning execution."""

    transition_id: str
    origin: str
    branch: str
    preserved_identity: str
    common_illah: str
    effective_description: str
    qadih_difference: str
    condition: str
    sabab: str
    preventer: Optional[str]
    transition_residuals: Tuple[Residual, ...]
    execution_rank: ExecutionRank
    minimal_complete_requirement: MinimalCompleteRequirement
    handoff: str
    evidence: Tuple[Evidence, ...]
    base_contract: Optional[RegistryTransitionContract] = None
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.transition_id:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: transition_id cannot be empty"
            )
        if not self.origin:
            raise ValueError(f"{FailureCode.M_02_02.value}: origin cannot be empty")
        if not self.branch:
            raise ValueError(f"{FailureCode.M_02_03.value}: branch cannot be empty")
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if not self.evidence:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: evidence cannot be empty"
            )
        if self.base_contract is not None:
            if self.base_contract.origin_ref != self.origin:
                raise ValueError(
                    f"{FailureCode.M_CX_01.value}: base_contract origin mismatch"
                )
            if self.base_contract.branch_ref != self.branch:
                raise ValueError(
                    f"{FailureCode.M_CX_01.value}: base_contract branch mismatch"
                )


@dataclass(frozen=True)
class EuclideanGateDecision:
    """Gate decision with constitutional rank and residual payload."""

    allowed: bool
    decision_rank: ExecutionRank
    reason: str
    transition_residuals: Tuple[Residual, ...]
    handoff: Optional[str]
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.reason:
            raise ValueError(f"{FailureCode.M_CX_02.value}: reason cannot be empty")
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class EuclideanFailureRecord:
    """Failure artifact produced when a transition is rejected/deferred."""

    failed_transition: str
    missing_condition: Optional[str]
    active_preventer: Optional[str]
    blocking_residual: Optional[str]
    closest_valid_stage: str
    required_handoff: Optional[str]
    repair_suggestion: Optional[str]
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.failed_transition:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: failed_transition cannot be empty"
            )
        if not self.closest_valid_stage:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: closest_valid_stage cannot be empty"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class LearningMemory:
    """Immutable learning memory of contracts and failure records."""

    contracts: Tuple[EuclideanTransitionContract, ...] = ()
    failures: Tuple[EuclideanFailureRecord, ...] = ()
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class RankedBranchPrediction:
    """Constitutional prediction over licensed next branches."""

    branch: str
    decision_rank: ExecutionRank
    transition_residuals: Tuple[Residual, ...]
    reason: str
    handoff: Optional[str]
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.branch:
            raise ValueError(f"{FailureCode.M_CX_02.value}: branch cannot be empty")
        if not self.reason:
            raise ValueError(f"{FailureCode.M_CX_02.value}: reason cannot be empty")
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


class Layer(str, Enum):
    """Staged Euclidean learning layers for energy guard checks."""

    T8_PHONIC_SIGNIFIER = "T8_PHONIC_SIGNIFIER"
    T9_RAW_MEANING = "T9_RAW_MEANING"
    T10_CONVENTIONAL = "T10_CONVENTIONAL"
    T11_RELATION = "T11_RELATION"
    T12_IFADAH = "T12_IFADAH"
    T13_HUKM = "T13_HUKM"


LAYER_MAX_RANK: Dict[Layer, ExecutionRank] = {
    Layer.T8_PHONIC_SIGNIFIER: ExecutionRank.LICENSED,
    Layer.T9_RAW_MEANING: ExecutionRank.CANDIDATE,
    Layer.T10_CONVENTIONAL: ExecutionRank.HYPOTHESIS,
    Layer.T11_RELATION: ExecutionRank.LICENSED,
    Layer.T12_IFADAH: ExecutionRank.LICENSED,
    Layer.T13_HUKM: ExecutionRank.CERTIFIED,
}


FORBIDDEN_OVERREACH: Dict[Layer, FrozenSet[str]] = {
    Layer.T9_RAW_MEANING: frozenset({"RelationClosed", "IfadahClosed", "Hukm"}),
    Layer.T10_CONVENTIONAL: frozenset({"IfadahClosed", "Hukm"}),
    Layer.T11_RELATION: frozenset({"CertifiedHukm"}),
    Layer.T12_IFADAH: frozenset({"RealityCertifiedHukm"}),
}


def _rank_value(rank: ExecutionRank) -> int:
    return _RANK_ORDER.index(rank)


def contract_from_registry(
    base_contract: RegistryTransitionContract,
    *,
    transition_id: str,
    execution_rank: ExecutionRank,
    handoff: str,
    evidence: Tuple[Evidence, ...],
    transition_residuals: Tuple[Residual, ...] = (),
    minimal_complete_requirement: Optional[MinimalCompleteRequirement] = None,
) -> EuclideanTransitionContract:
    """Create extended Euclidean learning contract from registry contract."""
    requirement = minimal_complete_requirement or MinimalCompleteRequirement(
        required_fields=(
            "origin",
            "branch",
            "preserved_identity",
            "common_illah",
            "effective_description",
            "qadih_difference",
            "condition",
            "sabab",
            "handoff",
            "evidence",
        ),
        forbidden_overreach=frozenset(),
        max_rank=ExecutionRank.CERTIFIED,
    )
    identity = ",".join(sorted(base_contract.preserved_identity))
    return EuclideanTransitionContract(
        transition_id=transition_id,
        origin=base_contract.origin_ref,
        branch=base_contract.branch_ref,
        preserved_identity=identity,
        common_illah=base_contract.common_illah,
        effective_description=base_contract.effective_description,
        qadih_difference=base_contract.qadih_difference_rule,
        condition=base_contract.condition,
        sabab=base_contract.cause,
        preventer=None,
        transition_residuals=transition_residuals,
        execution_rank=execution_rank,
        minimal_complete_requirement=requirement,
        handoff=handoff,
        evidence=evidence,
        base_contract=base_contract,
    )


def has_blocking_residual(contract: EuclideanTransitionContract) -> bool:
    """Return True when any residual is classified as blocking."""
    return any(r.kind == ResidualKind.BLOCKING for r in contract.transition_residuals)


def minimal_complete_is_satisfied(contract: EuclideanTransitionContract) -> bool:
    """Validate minimal complete requirement for the transition contract."""
    req = contract.minimal_complete_requirement

    fields = {
        "origin": contract.origin,
        "branch": contract.branch,
        "preserved_identity": contract.preserved_identity,
        "common_illah": contract.common_illah,
        "effective_description": contract.effective_description,
        "qadih_difference": contract.qadih_difference,
        "condition": contract.condition,
        "sabab": contract.sabab,
        "handoff": contract.handoff,
        "evidence": contract.evidence,
    }

    for field_name in req.required_fields:
        if not fields.get(field_name):
            return False

    if _rank_value(contract.execution_rank) > _rank_value(req.max_rank):
        return False

    return True


def evaluate_transition(contract: EuclideanTransitionContract) -> EuclideanGateDecision:
    """Evaluate full Euclidean transition contract as a gate decision."""
    if not contract.origin:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Missing origin",
            contract.transition_residuals,
            None,
        )

    if not contract.branch:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Missing branch",
            contract.transition_residuals,
            None,
        )

    if not contract.preserved_identity:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Identity not preserved",
            contract.transition_residuals,
            None,
        )

    if not contract.common_illah:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Missing common illah",
            contract.transition_residuals,
            None,
        )

    if not contract.effective_description:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Missing effective description",
            contract.transition_residuals,
            None,
        )

    if not contract.qadih_difference:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Qadih difference not checked",
            contract.transition_residuals,
            None,
        )

    if not contract.condition:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Condition not satisfied",
            contract.transition_residuals,
            None,
        )

    if not contract.sabab:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Sabab not active",
            contract.transition_residuals,
            None,
        )

    if contract.preventer:
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            f"Active preventer: {contract.preventer}",
            contract.transition_residuals,
            None,
        )

    if has_blocking_residual(contract):
        return EuclideanGateDecision(
            False,
            ExecutionRank.BLOCKED,
            "Blocking residual exists",
            contract.transition_residuals,
            None,
        )

    if not minimal_complete_is_satisfied(contract):
        return EuclideanGateDecision(
            False,
            ExecutionRank.DEFERRED,
            "Minimal complete requirement not satisfied",
            contract.transition_residuals,
            None,
        )

    if not contract.handoff:
        return EuclideanGateDecision(
            False,
            ExecutionRank.DEFERRED,
            "Missing handoff",
            contract.transition_residuals,
            None,
        )

    return EuclideanGateDecision(
        True,
        contract.execution_rank,
        "Transition licensed",
        contract.transition_residuals,
        contract.handoff,
    )


def suggest_repair(
    example: str,
    contract: EuclideanTransitionContract,
    decision: EuclideanGateDecision,
) -> Optional[str]:
    """Suggest constitutional repair path for a failed transition."""
    if contract.preventer:
        return f"Remove preventer: {contract.preventer}"
    if not contract.condition:
        return "Complete the missing condition"
    if has_blocking_residual(contract):
        return "Resolve blocking residual before transition"
    if not contract.handoff:
        return "Declare handoff target"
    if not decision.allowed:
        return f"Review transition contract for example: {example}"
    return None


def to_failure_record(
    example: str,
    contract: EuclideanTransitionContract,
    decision: EuclideanGateDecision,
) -> EuclideanFailureRecord:
    """Convert a gate decision into a failure learning artifact."""
    blocking = next(
        (r.code for r in contract.transition_residuals if r.kind == ResidualKind.BLOCKING),
        None,
    )

    missing_condition = None
    if not contract.condition:
        missing_condition = "missing_condition"

    return EuclideanFailureRecord(
        failed_transition=f"{contract.origin} -> {contract.branch}",
        missing_condition=missing_condition,
        active_preventer=contract.preventer,
        blocking_residual=blocking,
        closest_valid_stage=contract.origin,
        required_handoff=contract.handoff or None,
        repair_suggestion=suggest_repair(example, contract, decision),
    )


def learn_success(
    memory: LearningMemory,
    example: str,
    contract: EuclideanTransitionContract,
) -> Tuple[LearningMemory, EuclideanGateDecision]:
    """Learn from success; failed outcomes are redirected to failure memory."""
    decision = evaluate_transition(contract)
    if not decision.allowed:
        failure = to_failure_record(example, contract, decision)
        return LearningMemory(
            contracts=memory.contracts,
            failures=memory.failures + (failure,),
        ), decision

    return LearningMemory(
        contracts=memory.contracts + (contract,),
        failures=memory.failures,
    ), decision


def learn_failure(
    memory: LearningMemory,
    example: str,
    contract: EuclideanTransitionContract,
) -> Tuple[LearningMemory, EuclideanFailureRecord]:
    """Always learn failure artifact from a transition evaluation."""
    decision = evaluate_transition(contract)
    failure = to_failure_record(example, contract, decision)
    return LearningMemory(
        contracts=memory.contracts,
        failures=memory.failures + (failure,),
    ), failure


def predict_branch(
    memory: LearningMemory,
    origin: str,
) -> Tuple[RankedBranchPrediction, ...]:
    """Predict constitutionally licensed next branches for a given origin."""
    predictions: list[RankedBranchPrediction] = []

    for contract in memory.contracts:
        if contract.origin != origin:
            continue

        decision = evaluate_transition(contract)
        predictions.append(
            RankedBranchPrediction(
                branch=contract.branch,
                decision_rank=decision.decision_rank,
                transition_residuals=decision.transition_residuals,
                reason=decision.reason,
                handoff=decision.handoff,
            )
        )

    predictions.sort(key=lambda item: _rank_value(item.decision_rank), reverse=True)
    return tuple(predictions)


def energy_guard(
    layer: Layer,
    produced_outputs: FrozenSet[str],
    execution_rank: ExecutionRank,
) -> EuclideanGateDecision:
    """Block layer overreach and rank ceiling violations before transition gate."""
    forbidden = FORBIDDEN_OVERREACH.get(layer, frozenset())
    overlap = forbidden.intersection(produced_outputs)

    if overlap:
        return EuclideanGateDecision(
            allowed=False,
            decision_rank=ExecutionRank.BLOCKED,
            reason=(
                f"Overreach: layer {layer.value} produced forbidden outputs "
                f"{sorted(overlap)}"
            ),
            transition_residuals=(
                Residual(
                    code="LAYER_OVERREACH",
                    kind=ResidualKind.BLOCKING,
                    message="Layer attempted to solve a higher-layer task",
                ),
            ),
            handoff=None,
        )

    if _rank_value(execution_rank) > _rank_value(LAYER_MAX_RANK[layer]):
        return EuclideanGateDecision(
            allowed=False,
            decision_rank=ExecutionRank.DEFERRED,
            reason="Rank exceeds layer maximum",
            transition_residuals=(),
            handoff=None,
        )

    return EuclideanGateDecision(
        allowed=True,
        decision_rank=execution_rank,
        reason="Energy guard satisfied",
        transition_residuals=(),
        handoff=None,
    )


def euclidean_learning_step(
    memory: LearningMemory,
    example: str,
    layer: Layer,
    contract: EuclideanTransitionContract,
    produced_outputs: FrozenSet[str],
) -> Tuple[LearningMemory, EuclideanGateDecision]:
    """Run one full learning step: energy guard, transition gate, learning write."""
    energy = energy_guard(layer, produced_outputs, contract.execution_rank)

    if not energy.allowed:
        failure = to_failure_record(example, contract, energy)
        return LearningMemory(
            contracts=memory.contracts,
            failures=memory.failures + (failure,),
        ), energy

    decision = evaluate_transition(contract)
    if decision.allowed:
        return LearningMemory(
            contracts=memory.contracts + (contract,),
            failures=memory.failures,
        ), decision

    failure = to_failure_record(example, contract, decision)
    return LearningMemory(
        contracts=memory.contracts,
        failures=memory.failures + (failure,),
    ), decision


__all__ = [
    "ExecutionRank",
    "ResidualKind",
    "Residual",
    "Evidence",
    "MinimalCompleteRequirement",
    "EuclideanTransitionContract",
    "EuclideanGateDecision",
    "EuclideanFailureRecord",
    "LearningMemory",
    "RankedBranchPrediction",
    "Layer",
    "LAYER_MAX_RANK",
    "FORBIDDEN_OVERREACH",
    "contract_from_registry",
    "has_blocking_residual",
    "minimal_complete_is_satisfied",
    "evaluate_transition",
    "suggest_repair",
    "to_failure_record",
    "learn_success",
    "learn_failure",
    "predict_branch",
    "energy_guard",
    "euclidean_learning_step",
]
