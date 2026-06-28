"""
Audit-only Runtime Embargo Lift request contracts.

Origin: docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
Authority: docs/00_MAQOOL_CONSTITUTION.md §5; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode

Rank = Literal["CANDIDATE"]
RuntimeLiftArtifactKind = Literal["MODULE", "TEST", "DOC", "DATA", "SCHEMA"]
RuntimeLiftRequestSource = Literal[
    "RUNTIME_EMBARGO_LIFT_PR",
    "PROMPT",
    "USER_DELEGATION",
    "AGENT_RESPONSE",
    "READINESS_STATUS",
]
RuntimeLiftStatus = Literal["EXTERNALLY_BLOCKED"]
RuntimeLiftAuditStatus = Literal[
    "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
    "AUDIT_SHAPE_BLOCKED",
]

RUNTIME_LIFT_TRACE_REF = "docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md"
_VALID_ARTIFACT_KINDS = frozenset({"MODULE", "TEST", "DOC", "DATA", "SCHEMA"})
_VALID_REQUEST_SOURCE = "RUNTIME_EMBARGO_LIFT_PR"
_VALID_RUNTIME_STATUS = "EXTERNALLY_BLOCKED"
_VALID_AUDIT_STATUSES = frozenset(
    {
        "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
        "AUDIT_SHAPE_BLOCKED",
    }
)
_FORBIDDEN_ARTIFACT_PATH_PARTS = ("*", "~", "..", "//", "\\", "\x00", "\r", "\n", "\t")
_BROAD_ARTIFACT_SCOPES = frozenset({"runtime", "src/taaqqul_slot_geometry/runtime"})


def _require_trace_ref(trace_ref: str) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)


def _require_candidate_rank(rank: str) -> None:
    if rank != "CANDIDATE":
        raise ValueError(FailureCode.M_01_16.value)


def _require_non_empty(value: str) -> None:
    if not value:
        raise ValueError(FailureCode.M_00_22.value)


def _validate_artifact_path(artifact_path: str) -> None:
    if not artifact_path:
        raise ValueError(FailureCode.M_00_22.value)
    if artifact_path.startswith("/"):
        raise ValueError(FailureCode.M_00_22.value)
    if artifact_path.endswith("/"):
        raise ValueError(FailureCode.M_00_22.value)
    if artifact_path in _BROAD_ARTIFACT_SCOPES:
        raise ValueError(FailureCode.M_CX_02.value)
    if ":" in artifact_path:
        raise ValueError(FailureCode.M_00_22.value)
    if any(forbidden in artifact_path for forbidden in _FORBIDDEN_ARTIFACT_PATH_PARTS):
        raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class RuntimeLiftArtifact:
    """Exact future artifact shape; not runtime authorization.

    trace_ref: docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
    """

    artifact_path: str
    artifact_kind: RuntimeLiftArtifactKind
    exact_scope_only: bool
    trace_ref: str = RUNTIME_LIFT_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _validate_artifact_path(self.artifact_path)
        if self.artifact_kind not in _VALID_ARTIFACT_KINDS:
            raise ValueError(FailureCode.M_00_22.value)
        if self.exact_scope_only is not True:
            raise ValueError(FailureCode.M_CX_02.value)
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)


@dataclass(frozen=True)
class RuntimeLiftRequest:
    """Audit-only future lift request shape; runtime remains externally blocked.

    trace_ref: docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
    """

    request_id: str
    request_source_type: RuntimeLiftRequestSource
    pr_ref: str
    requested_artifacts: Tuple[RuntimeLiftArtifact, ...]
    authority_refs: Tuple[str, ...]
    failure_alignment_ref: str
    proof_policy_ref: str
    rollback_policy_ref: str
    external_blockage_acknowledged: bool
    prompt_delegation_disclaimed: bool
    runtime_status: RuntimeLiftStatus = "EXTERNALLY_BLOCKED"
    trace_ref: str = RUNTIME_LIFT_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty(self.request_id)
        if self.request_source_type != _VALID_REQUEST_SOURCE:
            raise ValueError(FailureCode.M_CX_02.value)
        if not self.pr_ref or ("PR" not in self.pr_ref and "#" not in self.pr_ref):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.requested_artifacts:
            raise ValueError(FailureCode.M_00_22.value)
        if not all(isinstance(artifact, RuntimeLiftArtifact) for artifact in self.requested_artifacts):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.authority_refs or not all(self.authority_refs):
            raise ValueError(FailureCode.M_00_22.value)
        _require_non_empty(self.failure_alignment_ref)
        _require_non_empty(self.proof_policy_ref)
        _require_non_empty(self.rollback_policy_ref)
        if self.external_blockage_acknowledged is not True:
            raise ValueError(FailureCode.M_CX_02.value)
        if self.prompt_delegation_disclaimed is not True:
            raise ValueError(FailureCode.M_CX_02.value)
        if self.runtime_status != _VALID_RUNTIME_STATUS:
            raise ValueError(FailureCode.M_CX_02.value)
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)


@dataclass(frozen=True)
class RuntimeLiftAuditResult:
    """Audit result for shape validation; never authorizes runtime.

    trace_ref: docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
    """

    request_id: str
    shape_valid: bool
    runtime_lift_authorized: bool
    status: RuntimeLiftAuditStatus
    blocking_reasons: Tuple[str, ...]
    checked_artifacts: Tuple[str, ...]
    trace_ref: str = RUNTIME_LIFT_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_non_empty(self.request_id)
        if self.runtime_lift_authorized is not False:
            raise ValueError(FailureCode.M_CX_02.value)
        if self.status not in _VALID_AUDIT_STATUSES:
            raise ValueError(FailureCode.M_CX_02.value)
        if "OPEN" in self.status or "AUTHORIZED" in self.status:
            raise ValueError(FailureCode.M_CX_02.value)
        if not self.blocking_reasons:
            raise ValueError(FailureCode.M_00_22.value)
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)


def audit_runtime_lift_request_shape(request: RuntimeLiftRequest) -> RuntimeLiftAuditResult:
    """Validate a future lift request shape without producing runtime authority."""

    return RuntimeLiftAuditResult(
        request_id=request.request_id,
        shape_valid=True,
        runtime_lift_authorized=False,
        status="AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED",
        blocking_reasons=("runtime_embargo_external_block_still_active",),
        checked_artifacts=tuple(
            artifact.artifact_path for artifact in request.requested_artifacts
        ),
        trace_ref=request.trace_ref,
        residuals=request.residuals,
    )
