"""Audit-only operation-boundary contracts and totalized transition protocol.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5, Rule 8
Authority: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md; docs/20_AGENT_AUTONOMY_RUNBOOK.md
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, FrozenSet, Mapping, Optional, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode

OperationBoundaryRank = str


class DomainGateStatus(str, Enum):
    PASS = "PASS"
    DELEGATED = "DELEGATED"
    BLOCKED = "BLOCKED"


class AuthorizationStatus(str, Enum):
    APPROVED = "APPROVED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    UNDEFINED = "UNDEFINED"
    FAILURE = "FAILURE"


class TotalizedStatus(str, Enum):
    SUCCESS = "Success"
    DEFERRED = "Deferred"
    BLOCKED = "Blocked"
    UNDEFINED = "Undefined"
    FAILURE = "Failure"


@dataclass(frozen=True)
class CandidateProposal:
    operation_id: str
    input_ids: Tuple[str, ...]
    input_types: Tuple[str, ...]
    domain: str
    evidence_ids: Tuple[str, ...] = ()
    expected_effect: str = ""
    trace_ref: str = "docs/20_AGENT_AUTONOMY_RUNBOOK.md"
    rank: OperationBoundaryRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise ValueError(FailureCode.M_CX_02.value)
        if not self.input_ids or any(not item for item in self.input_ids):
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.input_types or any(not item for item in self.input_types):
            raise ValueError(FailureCode.M_CX_21.value)
        if not self.domain:
            raise ValueError(FailureCode.M_CX_26.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class OperationContract:
    operation_id: str
    source_types: FrozenSet[str]
    target_type: str
    domain: str
    licensed_domain_bridges: FrozenSet[str]
    delegated_domain_bridges: FrozenSet[str] = field(default_factory=frozenset)
    preconditions: FrozenSet[str] = field(default_factory=frozenset)
    evidence_policy: FrozenSet[str] = field(default_factory=frozenset)
    blockers: FrozenSet[str] = field(default_factory=frozenset)
    preserved_identity_keys: FrozenSet[str] = field(default_factory=frozenset)
    closure_policy_ref: str = "policy:audit-only"
    transition_policy_ref: str = "policy:audit-only"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8"
    rank: OperationBoundaryRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise ValueError(FailureCode.M_CX_02.value)
        if not self.source_types or any(not item for item in self.source_types):
            raise ValueError(FailureCode.M_CX_21.value)
        if not self.target_type:
            raise ValueError(FailureCode.M_CX_22.value)
        if not self.domain:
            raise ValueError(FailureCode.M_CX_26.value)
        if not self.licensed_domain_bridges:
            raise ValueError(FailureCode.M_CX_03.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class AuthorizationContext:
    source_domain: str
    target_domain: str
    available_preconditions: FrozenSet[str] = field(default_factory=frozenset)
    available_evidence: FrozenSet[str] = field(default_factory=frozenset)
    active_blockers: FrozenSet[str] = field(default_factory=frozenset)
    source_identity: Mapping[str, str] = field(default_factory=dict)
    target_identity: Mapping[str, str] = field(default_factory=dict)
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7"
    rank: OperationBoundaryRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.source_domain or not self.target_domain:
            raise ValueError(FailureCode.M_CX_26.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class CheckEntry:
    stage: str
    outcome: str
    code: str
    detail: str


@dataclass(frozen=True)
class ApprovedTransitionContext:
    proposal: CandidateProposal
    contract: OperationContract
    context: AuthorizationContext
    checks: Tuple[CheckEntry, ...]
    trace_ref: str = "docs/20_AGENT_AUTONOMY_RUNBOOK.md"
    rank: OperationBoundaryRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.checks:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class AuthorizationResult:
    status: AuthorizationStatus
    checks: Tuple[CheckEntry, ...]
    approved_context: Optional[ApprovedTransitionContext]
    residuals: FrozenSet[str] = field(default_factory=frozenset)
    trace_ref: str = "docs/20_AGENT_AUTONOMY_RUNBOOK.md"
    rank: OperationBoundaryRank = "CANDIDATE"

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class TraceEvent:
    input_ids: Tuple[str, ...]
    operation_id: str
    evidence_ids: Tuple[str, ...]
    checks: Tuple[CheckEntry, ...]
    output_id: str
    residuals: FrozenSet[str]
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: OperationBoundaryRank = "CANDIDATE"

    def __post_init__(self) -> None:
        if not self.input_ids or not self.operation_id or not self.output_id:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class TransitionResult:
    status: TotalizedStatus
    output_id: str
    closure_state: str
    next_transitions: Tuple[str, ...]
    checks: Tuple[CheckEntry, ...]
    residuals: FrozenSet[str]
    trace: Optional[TraceEvent]
    trace_ref: str = "docs/20_AGENT_AUTONOMY_RUNBOOK.md"
    rank: OperationBoundaryRank = "CANDIDATE"

    def __post_init__(self) -> None:
        if not self.output_id:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


def _type_check(proposal: CandidateProposal, contract: OperationContract) -> Optional[CheckEntry]:
    if set(proposal.input_types).issubset(contract.source_types):
        return None
    unexpected = sorted(set(proposal.input_types) - set(contract.source_types))
    return CheckEntry(
        stage="TypeCheck",
        outcome="FAIL",
        code=FailureCode.M_CX_21.value,
        detail=f"TYPE_MISMATCH: expected={sorted(contract.source_types)} received={unexpected}",
    )


def _domain_check(contract: OperationContract, context: AuthorizationContext) -> tuple[DomainGateStatus, CheckEntry]:
    bridge = f"{context.source_domain}->{context.target_domain}"
    if bridge in contract.licensed_domain_bridges:
        return (
            DomainGateStatus.PASS,
            CheckEntry("DomainCheck", "PASS", "DOMAIN_BRIDGE_LICENSED", bridge),
        )
    if bridge in contract.delegated_domain_bridges:
        return (
            DomainGateStatus.DELEGATED,
            CheckEntry("DomainCheck", "DELEGATED", "DOMAIN_PATH_AUDIT_REQUIRED", bridge),
        )
    return (
        DomainGateStatus.BLOCKED,
        CheckEntry("DomainCheck", "BLOCKED", FailureCode.M_CX_29.value, bridge),
    )


def _missing(required: FrozenSet[str], available: FrozenSet[str]) -> tuple[str, ...]:
    return tuple(sorted(required - available))


def authorize(
    proposal: CandidateProposal,
    contract: OperationContract,
    context: AuthorizationContext,
) -> AuthorizationResult:
    checks: list[CheckEntry] = []

    if proposal.operation_id != contract.operation_id:
        checks.append(
            CheckEntry(
                stage="OperationSelection",
                outcome="FAIL",
                code=FailureCode.M_CX_23.value,
                detail="OPERATION_MISMATCH",
            )
        )
        return AuthorizationResult(
            status=AuthorizationStatus.UNDEFINED,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({"OPERATION_MISMATCH"}),
        )

    type_failure = _type_check(proposal, contract)
    if type_failure is not None:
        checks.append(type_failure)
        return AuthorizationResult(
            status=AuthorizationStatus.UNDEFINED,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({"TYPE_MISMATCH"}),
        )
    checks.append(CheckEntry("TypeCheck", "PASS", "TYPE_OK", contract.target_type))

    domain_state, domain_entry = _domain_check(contract, context)
    checks.append(domain_entry)
    if domain_state == DomainGateStatus.BLOCKED:
        return AuthorizationResult(
            status=AuthorizationStatus.BLOCKED,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({"FORBIDDEN_DOMAIN_LEAP"}),
        )
    if domain_state == DomainGateStatus.DELEGATED:
        return AuthorizationResult(
            status=AuthorizationStatus.DEFERRED,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({"DOMAIN_BRIDGE_UNPROVEN"}),
        )

    missing_pre = _missing(contract.preconditions, context.available_preconditions)
    if missing_pre:
        checks.append(
            CheckEntry(
                "PreconditionsCheck",
                "DEFERRED",
                FailureCode.M_CX_27.value,
                f"MISSING_PRECONDITIONS:{','.join(missing_pre)}",
            )
        )
        return AuthorizationResult(
            status=AuthorizationStatus.DEFERRED,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({f"PRECONDITION_MISSING:{item}" for item in missing_pre}),
        )
    checks.append(CheckEntry("PreconditionsCheck", "PASS", "PRECONDITIONS_OK", ""))

    missing_evidence = _missing(contract.evidence_policy, context.available_evidence)
    if missing_evidence:
        checks.append(
            CheckEntry(
                "EvidenceCheck",
                "DEFERRED",
                FailureCode.M_03_02.value,
                f"MISSING_EVIDENCE:{','.join(missing_evidence)}",
            )
        )
        return AuthorizationResult(
            status=AuthorizationStatus.DEFERRED,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({f"EVIDENCE_MISSING:{item}" for item in missing_evidence}),
        )
    checks.append(CheckEntry("EvidenceCheck", "PASS", "EVIDENCE_OK", ""))

    active_blockers = sorted(contract.blockers & context.active_blockers)
    if active_blockers:
        checks.append(
            CheckEntry(
                "BlockerCheck",
                "BLOCKED",
                FailureCode.M_02_05.value,
                f"BLOCKING_RESIDUAL:{','.join(active_blockers)}",
            )
        )
        return AuthorizationResult(
            status=AuthorizationStatus.BLOCKED,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({f"BLOCKING_RESIDUAL:{item}" for item in active_blockers}),
        )
    checks.append(CheckEntry("BlockerCheck", "PASS", "NO_BLOCKER", ""))

    identity_breaks = [
        key
        for key in sorted(contract.preserved_identity_keys)
        if context.source_identity.get(key) != context.target_identity.get(key)
    ]
    if identity_breaks:
        checks.append(
            CheckEntry(
                "IdentityCheck",
                "FAIL",
                FailureCode.M_CX_01.value,
                f"IDENTITY_VIOLATION:{','.join(identity_breaks)}",
            )
        )
        return AuthorizationResult(
            status=AuthorizationStatus.FAILURE,
            checks=tuple(checks),
            approved_context=None,
            residuals=frozenset({f"IDENTITY_VIOLATION:{item}" for item in identity_breaks}),
        )

    checks.append(CheckEntry("IdentityCheck", "PASS", "IDENTITY_SAFE", ""))
    approved = ApprovedTransitionContext(
        proposal=proposal,
        contract=contract,
        context=context,
        checks=tuple(checks),
        residuals=proposal.residuals | contract.residuals | context.residuals,
    )
    return AuthorizationResult(
        status=AuthorizationStatus.APPROVED,
        checks=tuple(checks),
        approved_context=approved,
        residuals=approved.residuals,
    )


def execute_effect(
    approved_context: ApprovedTransitionContext,
    effect_executor: Callable[[ApprovedTransitionContext], str],
) -> str:
    return effect_executor(approved_context)


def process(
    proposal: CandidateProposal,
    contract: OperationContract,
    context: AuthorizationContext,
    effect_executor: Callable[[ApprovedTransitionContext], str],
    *,
    next_transition_hints: Tuple[str, ...] = (),
) -> TransitionResult:
    authorization = authorize(proposal=proposal, contract=contract, context=context)

    if authorization.status != AuthorizationStatus.APPROVED:
        mapped = {
            AuthorizationStatus.DEFERRED: TotalizedStatus.DEFERRED,
            AuthorizationStatus.BLOCKED: TotalizedStatus.BLOCKED,
            AuthorizationStatus.UNDEFINED: TotalizedStatus.UNDEFINED,
            AuthorizationStatus.FAILURE: TotalizedStatus.FAILURE,
        }[authorization.status]
        return TransitionResult(
            status=mapped,
            output_id=f"{proposal.operation_id}:no-output",
            closure_state="REOPEN_REQUIRED" if mapped == TotalizedStatus.FAILURE else "DEFERRED",
            next_transitions=(),
            checks=authorization.checks,
            residuals=authorization.residuals,
            trace=None,
        )

    approved_context = authorization.approved_context
    if approved_context is None:
        raise ValueError(FailureCode.M_CX_08.value)

    checks = list(authorization.checks)
    output_id = execute_effect(approved_context, effect_executor)
    checks.append(CheckEntry("ExecuteEffect", "PASS", "EFFECT_EXECUTED", output_id))
    checks.append(CheckEntry("RankBound", "PASS", "RANK_LIMITED_TO_CANDIDATE", ""))

    all_residuals = frozenset(
        set(authorization.residuals) | set(proposal.residuals) | set(contract.residuals) | set(context.residuals)
    )
    checks.append(CheckEntry("ResidualEmit", "PASS", "RESIDUALS_VISIBLE", str(len(all_residuals))))

    trace_event = TraceEvent(
        input_ids=proposal.input_ids,
        operation_id=proposal.operation_id,
        evidence_ids=proposal.evidence_ids,
        checks=tuple(checks),
        output_id=output_id,
        residuals=all_residuals,
    )
    checks.append(CheckEntry("TraceCommit", "PASS", "TRACE_COMMITTED", trace_event.output_id))

    closure_state = "CLOSED" if not all_residuals else "CLOSED_WITH_RESIDUALS"
    checks.append(CheckEntry("ClosureEvaluate", "PASS", closure_state, contract.closure_policy_ref))

    checks.append(
        CheckEntry(
            "TransitionReadiness",
            "PASS",
            "NEXT_TRANSITIONS_DECLARED",
            ",".join(next_transition_hints),
        )
    )

    return TransitionResult(
        status=TotalizedStatus.SUCCESS,
        output_id=output_id,
        closure_state=closure_state,
        next_transitions=next_transition_hints,
        checks=tuple(checks),
        residuals=all_residuals,
        trace=trace_event,
    )
