"""
Closure kernel for the minimal-mujarrad Euclidean flow.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1, Rule 5
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (L1 open)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank import Rank

Severity = Literal["note", "warning", "blocker"]
ResidualFamily = Literal[
    "identity",
    "path",
    "evidence",
    "scope",
    "relation",
    "phonology",
    "morphology",
    "orthography",
]
CertificateStatus = Literal["closed", "blocked", "provisional"]
ConflictStatus = Literal["separated", "coexistent", "blocked", "suspended", "provisional"]

_ALLOWED_LAYERS: Tuple[str, ...] = (
    "L0_Letter",
    "L1_Atom",
    "L2_Syllable",
    "L3_RootStem",
    "L4_MinimalMujarrad",
    "L5_Jamid",
    "L6_PastMujarradEvent",
    "L7_Augmented",
    "L8_Imperfect",
    "L9_Imperative",
    "L10_Derivation",
    "L11_MabniTool",
    "L12_Irab",
)

_ALLOWED_MOTION_STATES = frozenset({"فتحة", "ضمة", "كسرة", "سكون"})
_ALLOWED_CONFLICT_STATUSES = frozenset({"separated", "coexistent", "blocked", "suspended", "provisional"})
_ALLOWED_EVENT_PATTERNS = frozenset({"فَعَلَ", "فَعِلَ", "فَعُلَ"})
CONFLICT_MSG_BLOCKER_RESIDUAL = "blocker_residual_conflict"
CONFLICT_MSG_NASKH_NO_CHRONOLOGY = "naskh_like_without_chronology_evidence"
CONFLICT_MSG_TARJIH_PROVISIONAL = "provisional_tarjih_after_jam_failure"
CONFLICT_MSG_TARJIH_BLOCKED = "tarjih_blocked_until_jam_fails"
CONFLICT_MSG_UNRESOLVED_SUSPENDED = "unresolved_conflict_suspended"
_ALLOWED_AUGMENTED_PATTERNS = frozenset({
    "أفعل",
    "فعّل",
    "فاعل",
    "انفعل",
    "افتعل",
    "تفعّل",
    "تفاعل",
    "استفعل",
})
_ALLOWED_JAMID_ANCHORS = frozenset({"binary", "ternary"})
_ALLOWED_MABNI_TOOL_BASE_LAYERS = frozenset({
    "L1_Atom",
    "L2_Syllable",
    "L3_RootStem",
    "L4_MinimalMujarrad",
    "L5_Jamid",
    "L10_Derivation",
})
_ALLOWED_I3RAB_CARRIER_LAYERS = frozenset({
    "L5_Jamid",
    "L6_PastMujarradEvent",
    "L8_Imperfect",
    "L10_Derivation",
    "L11_MabniTool",
})


def _validate_residual_structure(residuals: FrozenSet[str]) -> None:
    if not isinstance(residuals, frozenset) or any(not isinstance(item, str) for item in residuals):
        raise ValueError(FailureCode.M_CX_08.value)


@dataclass(frozen=True)
class Trace:
    trace_id: str
    source_layer: str
    evidence: Tuple[str, ...]
    timestamp: str | None = None
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_id:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.source_layer not in _ALLOWED_LAYERS:
            raise ValueError(FailureCode.M_CX_13.value)
        if not self.evidence:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class Residual:
    family: ResidualFamily
    severity: Severity
    message: str
    remediation_hint: str | None = None
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.message:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class Failure:
    failed_gate: str
    reason: str
    blocking_residuals: Tuple[Residual, ...]
    trace: Trace
    repair_hint: str
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.failed_gate or not self.reason or not self.repair_hint:
            raise ValueError(FailureCode.M_CX_08.value)
        if any(r.severity != "blocker" for r in self.blocking_residuals):
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class ClosureCertificate:
    layer: str
    status: CertificateStatus
    identity_preserved: bool
    boundary_declared: bool
    trace: Trace
    residual_entries: Tuple[Residual, ...]
    next_permissions: Tuple[str, ...]
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.layer not in _ALLOWED_LAYERS:
            raise ValueError(FailureCode.M_CX_13.value)
        if self.status not in {"closed", "blocked", "provisional"}:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)
        invalid_permissions = {
            p for p in self.next_permissions if p not in _ALLOWED_LAYERS
        }
        if invalid_permissions:
            raise ValueError(FailureCode.M_CX_04.value)
        _validate_residual_structure(self.residuals)


@dataclass(frozen=True)
class PhoneticAtom:
    letter: str
    motion: str
    trace: Trace
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.letter:
            raise ValueError(FailureCode.M_00_14.value)
        if self.motion not in _ALLOWED_MOTION_STATES:
            raise ValueError(FailureCode.M_00_04.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class RootCandidate:
    radicals: Tuple[str, ...]
    positions: Tuple[str, ...]
    root_type: str
    closure: ClosureCertificate
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if len(self.radicals) < 3:
            raise ValueError(FailureCode.M_00_22.value)
        if len(self.positions) != len(self.radicals):
            raise ValueError(FailureCode.M_CX_01.value)
        if not self.root_type:
            raise ValueError(FailureCode.M_00_22.value)
        if self.closure.layer != "L3_RootStem":
            raise ValueError(FailureCode.M_CX_02.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class MujarradCandidate:
    path: Literal["jamid", "event"]
    pattern: str | None
    root: RootCandidate
    closure: ClosureCertificate
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.path not in {"jamid", "event"}:
            raise ValueError(FailureCode.M_00_22.value)
        if self.closure.layer != "L4_MinimalMujarrad":
            raise ValueError(FailureCode.M_CX_02.value)
        if self.path == "event" and self.pattern not in _ALLOWED_EVENT_PATTERNS:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class DerivationCandidate:
    origin: MujarradCandidate
    derivation_type: str
    added_units: Tuple[str, ...]
    illah_or_function: str | None
    closure: ClosureCertificate
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.derivation_type:
            raise ValueError(FailureCode.M_00_22.value)
        if self.closure.layer not in {"L7_Augmented", "L10_Derivation"}:
            raise ValueError(FailureCode.M_CX_02.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class ProvisionalCertificate:
    closed_layers: Tuple[str, ...]
    provisional_layers: Tuple[str, ...]
    blocked_layers: Tuple[str, ...]
    allowed_next_steps: Tuple[str, ...]
    residual_matrix: Tuple[Residual, ...]
    failure_matrix: Tuple[Failure, ...]
    evidence_rank_label: str
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.evidence_rank_label:
            raise ValueError(FailureCode.M_CX_08.value)
        unknown_layers = {
            layer
            for layer in (
                *self.closed_layers,
                *self.provisional_layers,
                *self.blocked_layers,
                *self.allowed_next_steps,
            )
            if layer not in _ALLOWED_LAYERS
        }
        if unknown_layers:
            raise ValueError(FailureCode.M_CX_13.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class ConflictClaim:
    certificate: ClosureCertificate
    domain_scope: str
    coexistence_permitted: bool = False
    naskh_like_claim: bool = False
    chronology_evidence: Tuple[str, ...] = ()
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.domain_scope:
            raise ValueError(FailureCode.M_CX_08.value)
        if getattr(self.certificate, "trace", None) is None:
            raise ValueError(FailureCode.M_CX_08.value)
        if not getattr(self.certificate.trace, "trace_id", ""):
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)
        _validate_residual_structure(self.residuals)


@dataclass(frozen=True)
class ConflictCertificate:
    status: ConflictStatus
    resolution_path: Tuple[str, ...]
    candidate_layers: Tuple[str, ...]
    candidate_trace_ids: Tuple[str, ...]
    residual_entries: Tuple[Residual, ...]
    has_blocked_claims: bool
    blocked_transition: bool
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.status not in _ALLOWED_CONFLICT_STATUSES:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.candidate_layers or not self.candidate_trace_ids:
            raise ValueError(FailureCode.M_CX_08.value)
        if len(self.candidate_layers) != len(self.candidate_trace_ids):
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)
        _validate_residual_structure(self.residuals)


@dataclass(frozen=True)
class CoverageCaseRow:
    case_id: str
    layer: str
    gate_name: str
    expected_status: CertificateStatus
    observed_status: CertificateStatus | None = None
    note: str | None = None
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.case_id:
            raise ValueError(FailureCode.M_CX_08.value)
        if self.layer not in _ALLOWED_LAYERS:
            raise ValueError(FailureCode.M_CX_13.value)
        if not self.gate_name:
            raise ValueError(FailureCode.M_CX_08.value)
        if self.expected_status not in {"closed", "blocked", "provisional"}:
            raise ValueError(FailureCode.M_CX_08.value)
        if self.observed_status is not None and self.observed_status not in {
            "closed",
            "blocked",
            "provisional",
        }:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class CoverageMatrix:
    rows: Tuple[CoverageCaseRow, ...] = ()
    claimed_exhaustive: bool = False
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.claimed_exhaustive:
            raise ValueError(FailureCode.M_CX_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)

    def register_case_row(self, row: CoverageCaseRow) -> "CoverageMatrix":
        if any(existing.case_id == row.case_id for existing in self.rows):
            raise ValueError(FailureCode.M_CX_04.value)
        return CoverageMatrix(
            rows=(*self.rows, row),
            claimed_exhaustive=False,
        )


def _certificate_status(
    *,
    identity_preserved: bool,
    boundary_declared: bool,
    trace_recorded: bool,
    residuals_audited: bool,
    next_layer_permission: bool,
    residuals: Tuple[Residual, ...],
) -> CertificateStatus:
    if not all((
        identity_preserved,
        boundary_declared,
        trace_recorded,
        residuals_audited,
        next_layer_permission,
    )):
        return "blocked"
    has_blocker = any(r.severity == "blocker" for r in residuals)
    if has_blocker:
        return "blocked"
    if residuals:
        return "provisional"
    return "closed"


def make_closure_certificate(
    *,
    layer: str,
    identity_preserved: bool,
    boundary_declared: bool,
    trace: Trace,
    residual_entries: Tuple[Residual, ...] = (),
    next_permissions: Tuple[str, ...] = (),
    requires_next_permission: bool = True,
) -> ClosureCertificate:
    trace_recorded = bool(trace.trace_id)
    residuals_audited = True
    next_layer_permission = bool(next_permissions) if requires_next_permission else True
    status = _certificate_status(
        identity_preserved=identity_preserved,
        boundary_declared=boundary_declared,
        trace_recorded=trace_recorded,
        residuals_audited=residuals_audited,
        next_layer_permission=next_layer_permission,
        residuals=residual_entries,
    )
    residual_codes = frozenset(f"{r.family}:{r.message}" for r in residual_entries)
    return ClosureCertificate(
        layer=layer,
        status=status,
        identity_preserved=identity_preserved,
        boundary_declared=boundary_declared,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=next_permissions,
        residuals=residual_codes,
    )


def should_block_transition(certificate: ClosureCertificate) -> bool:
    return (
        certificate.status == "blocked"
        or any(r.severity == "blocker" for r in certificate.residual_entries)
    )


def issue_provisional_certificate(
    certificates: Tuple[ClosureCertificate, ...],
    failures: Tuple[Failure, ...] = (),
    evidence_rank_label: str = "candidate_evidence",
) -> ProvisionalCertificate:
    closed_layers = tuple(c.layer for c in certificates if c.status == "closed")
    provisional_layers = tuple(c.layer for c in certificates if c.status == "provisional")
    blocked_layers = tuple(c.layer for c in certificates if c.status == "blocked")
    allowed_next_steps = tuple(
        p
        for c in certificates
        if c.status in {"closed", "provisional"}
        for p in c.next_permissions
    )
    residual_matrix = tuple(r for c in certificates for r in c.residual_entries)
    has_blocker = any(r.severity == "blocker" for r in residual_matrix)
    if has_blocker:
        allowed_next_steps = tuple()
    residual_codes = frozenset(f"{r.family}:{r.message}" for r in residual_matrix)
    return ProvisionalCertificate(
        closed_layers=closed_layers,
        provisional_layers=provisional_layers,
        blocked_layers=blocked_layers,
        allowed_next_steps=allowed_next_steps,
        residual_matrix=residual_matrix,
        failure_matrix=failures,
        evidence_rank_label=evidence_rank_label,
        residuals=residual_codes,
    )


def _make_conflict_certificate(
    *,
    status: ConflictStatus,
    resolution_path: Tuple[str, ...],
    claims: Tuple[ConflictClaim, ...],
    residual_entries: Tuple[Residual, ...],
    has_blocked_claims: bool,
) -> ConflictCertificate:
    residual_identifiers = frozenset(f"{r.family}:{r.message}" for r in residual_entries)
    return ConflictCertificate(
        status=status,
        resolution_path=resolution_path,
        candidate_layers=tuple(claim.certificate.layer for claim in claims),
        candidate_trace_ids=tuple(claim.certificate.trace.trace_id for claim in claims),
        residual_entries=residual_entries,
        has_blocked_claims=has_blocked_claims,
        blocked_transition=(
            has_blocked_claims
            or status == "blocked"
            or any(item.severity == "blocker" for item in residual_entries)
        ),
        residuals=residual_identifiers,
    )


def _claim_has_blocker(claim: ConflictClaim) -> bool:
    certificate = claim.certificate
    return should_block_transition(certificate) or any(
        item.severity == "blocker" for item in certificate.residual_entries
    )


def resolve_closure_conflicts(
    *,
    claims: Tuple[ConflictClaim, ...],
    attempt_tarjih: bool = False,
) -> ConflictCertificate:
    if not claims:
        raise ValueError(FailureCode.M_CX_08.value)

    path = ["collect_candidate_certificates"]
    has_blocked_claims = any(_claim_has_blocker(claim) for claim in claims)

    domain_clusters = {
        domain: tuple(claim for claim in claims if claim.domain_scope == domain)
        for domain in {claim.domain_scope for claim in claims}
    }
    path.append("domain_clusters_computed")
    multi_claim_clusters = tuple(cluster for cluster in domain_clusters.values() if len(cluster) > 1)
    if not multi_claim_clusters:
        return _make_conflict_certificate(
            status="separated",
            resolution_path=(*path, "domain_separation"),
            claims=claims,
            residual_entries=(),
            has_blocked_claims=has_blocked_claims,
        )
    path.append("domain_conflict_clusters_detected")
    clustered_claims = tuple(claim for cluster in multi_claim_clusters for claim in cluster)

    jam_possible = all(claim.coexistence_permitted for claim in clustered_claims)
    if jam_possible:
        if attempt_tarjih:
            return _make_conflict_certificate(
                status="suspended",
                resolution_path=(*path, "jam_available", "tarjih_blocked"),
                claims=claims,
                residual_entries=(
                    Residual(
                        family="scope",
                        severity="blocker",
                        message=CONFLICT_MSG_TARJIH_BLOCKED,
                        remediation_hint="apply jam/coexistence first; tarjih is licensed only after jam failure",
                    ),
                ),
                has_blocked_claims=has_blocked_claims,
            )
        return _make_conflict_certificate(
            status="coexistent",
            resolution_path=(*path, "jam"),
            claims=claims,
            residual_entries=(),
            has_blocked_claims=has_blocked_claims,
        )
    path.append("jam_failed")

    if has_blocked_claims:
        return _make_conflict_certificate(
            status="blocked",
            resolution_path=(*path, "blocker_residual_conflict"),
            claims=claims,
            residual_entries=(
                Residual(
                    family="path",
                    severity="blocker",
                    message=CONFLICT_MSG_BLOCKER_RESIDUAL,
                    remediation_hint="clear blocker residuals in candidate certificates before transition",
                ),
            ),
            has_blocked_claims=has_blocked_claims,
        )

    naskh_like_claims = tuple(claim for claim in clustered_claims if claim.naskh_like_claim)
    if naskh_like_claims and any(not claim.chronology_evidence for claim in naskh_like_claims):
        return _make_conflict_certificate(
            status="suspended",
            resolution_path=(*path, "naskh_like_gate"),
            claims=claims,
            residual_entries=(
                Residual(
                    family="evidence",
                    severity="warning",
                    message=CONFLICT_MSG_NASKH_NO_CHRONOLOGY,
                    remediation_hint="model chronology evidence before opening naskh-like conflict handling",
                ),
            ),
            has_blocked_claims=has_blocked_claims,
        )

    if attempt_tarjih:
        return _make_conflict_certificate(
            status="provisional",
            resolution_path=(*path, "tarjih_after_jam_failure"),
            claims=claims,
            residual_entries=(
                Residual(
                    family="scope",
                    severity="note",
                    message=CONFLICT_MSG_TARJIH_PROVISIONAL,
                    remediation_hint="record tarjih as provisional conflict certificate only",
                ),
            ),
            has_blocked_claims=has_blocked_claims,
        )

    return _make_conflict_certificate(
        status="suspended",
        resolution_path=(*path, "suspend_unresolved"),
        claims=claims,
        residual_entries=(
            Residual(
                family="path",
                severity="warning",
                message=CONFLICT_MSG_UNRESOLVED_SUSPENDED,
                remediation_hint="keep conflict suspended until a licensed resolver is provided",
            ),
        ),
        has_blocked_claims=has_blocked_claims,
    )


def _require_lower_closure(
    *,
    lower_certificate: ClosureCertificate | None,
    expected_layers: FrozenSet[str],
    missing_message: str,
    missing_hint: str,
) -> Tuple[Residual, ...]:
    if lower_certificate is None:
        return (
            Residual(
                family="path",
                severity="blocker",
                message=missing_message,
                remediation_hint=missing_hint,
            ),
        )
    if lower_certificate.layer not in expected_layers:
        return (
            Residual(
                family="path",
                severity="blocker",
                message="required_lower_layer_mismatch",
                remediation_hint="provide the direct lower closure certificate for this gate",
            ),
        )
    if should_block_transition(lower_certificate):
        return (
            Residual(
                family="path",
                severity="blocker",
                message="required_lower_closure_blocked",
                remediation_hint="resolve blocker residuals in required lower closure first",
            ),
        )
    return ()


def weak_letter_gate(
    *,
    radicals: Tuple[str, ...],
    weak_letters: FrozenSet[str] = frozenset({"و", "ي", "ا"}),
) -> Tuple[bool, Tuple[Residual, ...]]:
    weak_positions = tuple(i for i, radical in enumerate(radicals) if radical in weak_letters)
    if not weak_positions:
        return True, ()
    residuals = tuple(
        Residual(
            family="morphology",
            severity="warning",
            message=f"weak_letter_at_position_{idx}",
            remediation_hint="declare weak-letter strategy: deletion/substitution/lengthening",
        )
        for idx in weak_positions
    )
    return True, residuals


def hamza_gate(*, radicals: Tuple[str, ...]) -> Tuple[bool, Tuple[Residual, ...]]:
    hamza_positions = tuple(i for i, radical in enumerate(radicals) if radical == "ء")
    if not hamza_positions:
        return True, ()
    residuals = tuple(
        Residual(
            family="orthography",
            severity="warning",
            message=f"hamza_position_{idx}",
            remediation_hint="declare hamza type/carrier and orthographic variation",
        )
        for idx in hamza_positions
    )
    return True, residuals


def gemination_gate(*, radicals: Tuple[str, ...]) -> Tuple[bool, Tuple[Residual, ...]]:
    if len(radicals) < 2:
        return True, ()
    repeated = tuple(i for i in range(1, len(radicals)) if radicals[i] == radicals[i - 1])
    if not repeated:
        return True, ()
    residuals = tuple(
        Residual(
            family="morphology",
            severity="warning",
            message=f"gemination_at_position_{idx}",
            remediation_hint="declare shadda as compressed double identity",
        )
        for idx in repeated
    )
    return True, residuals


def madd_gate(*, motion: str, extended: bool) -> Tuple[bool, Tuple[Residual, ...]]:
    if not extended:
        return True, ()
    if motion == "سكون":
        return False, (
            Residual(
                family="phonology",
                severity="blocker",
                message="madd_without_short_motion",
                remediation_hint="madd requires short motion before extension",
            ),
        )
    return True, (
        Residual(
            family="phonology",
            severity="warning",
            message="madd_extension_declared",
            remediation_hint="ensure extension is licensed by weak-letter carrier",
        ),
    )


def hamzat_wasl_gate(*, appears_in_start: bool, drops_in_connection: bool) -> Tuple[bool, Tuple[Residual, ...]]:
    if not appears_in_start:
        return True, ()
    if appears_in_start and not drops_in_connection:
        return False, (
            Residual(
                family="phonology",
                severity="blocker",
                message="hamzat_wasl_connection_rule_missing",
                remediation_hint="hamzat wasl must drop in connection",
            ),
        )
    return True, (
        Residual(
            family="phonology",
            severity="note",
            message="hamzat_wasl_profiled",
            remediation_hint="keep wasl onset support as non-root identity",
        ),
    )


def close_l3_root_stem(
    *,
    radicals: Tuple[str, ...],
    trace: Trace,
    positions: Tuple[str, ...] = ("فاء", "عين", "لام"),
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = ()
    if len(radicals) < 3:
        residual_entries += (
            Residual(
                family="identity",
                severity="blocker",
                message="missing_radical",
                remediation_hint="supply ordered radicals with preserved positions",
            )
        ,)

    _, weak_res = weak_letter_gate(radicals=radicals)
    _, hamza_res = hamza_gate(radicals=radicals)
    _, gem_res = gemination_gate(radicals=radicals)
    residual_entries += (*weak_res, *hamza_res, *gem_res)

    if len(positions) != len(radicals):
        residual_entries += (
            Residual(
                family="identity",
                severity="blocker",
                message="ambiguous_radical",
                remediation_hint="declare فاء/عين/لام positions explicitly",
            )
        ,)

    return make_closure_certificate(
        layer="L3_RootStem",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L4_MinimalMujarrad",),
    )


def close_l4_minimal_mujarrad(
    *,
    path: Literal["event", "jamid"],
    pattern: str | None,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=lower_certificate,
        expected_layers=frozenset({"L3_RootStem"}),
        missing_message="minimal_mujarrad_without_root_stem_closure",
        missing_hint="close L3 and clear blocker residuals before minimal mujarrad closure",
    )
    if path == "event" and pattern not in _ALLOWED_EVENT_PATTERNS:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="minimal_mujarrad_event_pattern_outside_set",
                remediation_hint="use one of فَعَلَ / فَعِلَ / فَعُلَ for event path",
            ),
        )
    if path == "jamid" and pattern is not None:
        residual_entries += (
            Residual(
                family="path",
                severity="warning",
                message="jamid_path_ignores_event_pattern",
                remediation_hint="omit pattern for jamid path",
            ),
        )
    return make_closure_certificate(
        layer="L4_MinimalMujarrad",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L5_Jamid", "L6_PastMujarradEvent", "L7_Augmented"),
    )


def close_l5_jamid_anchor(
    *,
    anchor_type: str,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=lower_certificate,
        expected_layers=frozenset({"L4_MinimalMujarrad"}),
        missing_message="jamid_without_minimal_mujarrad_closure",
        missing_hint="close L4 and clear blocker residuals before jamid anchoring",
    )
    if anchor_type not in _ALLOWED_JAMID_ANCHORS:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="jamid_anchor_outside_closed_set",
                remediation_hint="use binary or ternary jamid anchor only",
            ),
        )
    return make_closure_certificate(
        layer="L5_Jamid",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L11_MabniTool", "L12_Irab"),
    )


def close_l6_past_mujarrad_event(
    *,
    pattern: str,
    has_fa_il_slot: bool,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=lower_certificate,
        expected_layers=frozenset({"L4_MinimalMujarrad"}),
        missing_message="past_event_without_minimal_mujarrad_closure",
        missing_hint="close L4 and clear blocker residuals before past-event closure",
    )
    if pattern not in _ALLOWED_EVENT_PATTERNS:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="pattern_outside_minimal_past_set",
                remediation_hint="use one of فَعَلَ / فَعِلَ / فَعُلَ",
            )
        ,)
    if not has_fa_il_slot:
        residual_entries += (
            Residual(
                family="relation",
                severity="blocker",
                message="past_event_without_fa_il_slot",
                remediation_hint="declare fa'il relation before ifadah claim",
            )
        ,)
    return make_closure_certificate(
        layer="L6_PastMujarradEvent",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L7_Augmented", "L8_Imperfect", "L9_Imperative", "L10_Derivation"),
    )


def close_l7_augmented(
    *,
    augmentation_pattern: str,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=lower_certificate,
        expected_layers=frozenset({"L4_MinimalMujarrad", "L6_PastMujarradEvent"}),
        missing_message="augmentation_before_mujarrad",
        missing_hint="close L4/L6 and clear blocker residuals before opening augmented path",
    )
    if augmentation_pattern not in _ALLOWED_AUGMENTED_PATTERNS:
        residual_entries += (
            Residual(
                family="morphology",
                severity="blocker",
                message="added_letter_without_origin",
                remediation_hint="declare valid augmentation form and bounded effect",
            )
        ,)
    return make_closure_certificate(
        layer="L7_Augmented",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L8_Imperfect", "L10_Derivation"),
    )


def close_l8_imperfect_event(
    *,
    has_event_origin: bool,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=lower_certificate,
        expected_layers=frozenset({"L6_PastMujarradEvent", "L7_Augmented"}),
        missing_message="imperfect_without_lower_closure",
        missing_hint="close L6 or L7 and clear blocker residuals first",
    )
    if not has_event_origin:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="imperfect_without_event_origin",
                remediation_hint="declare event origin before imperfect closure",
            ),
        )
    return make_closure_certificate(
        layer="L8_Imperfect",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L9_Imperative", "L10_Derivation"),
    )


def close_l9_imperative_event(
    *,
    has_addressee_slot: bool,
    has_force_slot: bool,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=lower_certificate,
        expected_layers=frozenset({"L8_Imperfect"}),
        missing_message="imperative_without_lower_closure",
        missing_hint="close L8 and clear blocker residuals before imperative closure",
    )
    if not has_addressee_slot:
        residual_entries += (
            Residual(
                family="relation",
                severity="blocker",
                message="imperative_without_addressee_slot",
                remediation_hint="declare imperative addressee relation before closure",
            ),
        )
    if not has_force_slot:
        residual_entries += (
            Residual(
                family="relation",
                severity="blocker",
                message="imperative_without_force_slot",
                remediation_hint="declare force/jussive slot before imperative closure",
            ),
        )
    return make_closure_certificate(
        layer="L9_Imperative",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L10_Derivation",),
    )


def close_l10_derivation_family(
    *,
    has_mujarrad_origin: bool,
    has_event_origin: bool,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=lower_certificate,
        expected_layers=frozenset({"L9_Imperative", "L8_Imperfect", "L7_Augmented"}),
        missing_message="derivation_without_lower_closure",
        missing_hint="close L7/L8/L9 and clear blocker residuals before derivation closure",
    )
    if not has_mujarrad_origin:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="derivation_without_mujarrad_origin",
                remediation_hint="link derivation to a licensed mujarrad origin",
            ),
        )
    if not has_event_origin:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="derivation_without_event_origin",
                remediation_hint="link derivation to an event-origin closure",
            ),
        )
    return make_closure_certificate(
        layer="L10_Derivation",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L11_MabniTool",),
    )


def close_l11_mabni_tool_reference(
    *,
    forced_into_root_weight_path: bool,
    functional_identity_licensed: bool,
    lower_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = ()
    if lower_certificate is not None:
        residual_entries += _require_lower_closure(
            lower_certificate=lower_certificate,
            expected_layers=_ALLOWED_MABNI_TOOL_BASE_LAYERS,
            missing_message="mabni_tool_without_lower_closure",
            missing_hint="provide a licensed lower closure certificate for mabni/tool path",
        )
    elif not functional_identity_licensed:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="mabni_tool_without_functional_license",
                remediation_hint="license functional identity when opening standalone mabni/tool path",
            ),
        )
    if forced_into_root_weight_path:
        residual_entries += (
            Residual(
                family="scope",
                severity="blocker",
                message="mabni_tool_forced_into_root_weight_path",
                remediation_hint="keep mabni/tool/reference outside root-weight derivational path",
            ),
        )
    return make_closure_certificate(
        layer="L11_MabniTool",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=("L12_Irab",),
    )


def close_l12_i3rab_relation(
    *,
    has_syntactic_relation: bool,
    has_governing_factor: bool,
    carrier_certificate: ClosureCertificate | None,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = _require_lower_closure(
        lower_certificate=carrier_certificate,
        expected_layers=_ALLOWED_I3RAB_CARRIER_LAYERS,
        missing_message="i3rab_without_lower_closure",
        missing_hint="provide a licensed carrier closure and clear blocker residuals before i'rab closure",
    )
    if not has_syntactic_relation:
        residual_entries += (
            Residual(
                family="relation",
                severity="blocker",
                message="i3rab_without_syntactic_relation",
                remediation_hint="declare syntactic relation before i'rab closure",
            ),
        )
    if not has_governing_factor:
        residual_entries += (
            Residual(
                family="relation",
                severity="blocker",
                message="i3rab_without_governing_factor",
                remediation_hint="declare governing factor (عامل) before i'rab closure",
            ),
        )
    return make_closure_certificate(
        layer="L12_Irab",
        identity_preserved=True,
        boundary_declared=True,
        trace=trace,
        residual_entries=residual_entries,
        next_permissions=(),
        requires_next_permission=False,
    )


__all__ = [
    "ConflictCertificate",
    "ConflictClaim",
    "ConflictStatus",
    "CoverageCaseRow",
    "CoverageMatrix",
    "ClosureCertificate",
    "DerivationCandidate",
    "Failure",
    "MujarradCandidate",
    "PhoneticAtom",
    "ProvisionalCertificate",
    "Residual",
    "RootCandidate",
    "Trace",
    "close_l3_root_stem",
    "close_l4_minimal_mujarrad",
    "close_l5_jamid_anchor",
    "close_l6_past_mujarrad_event",
    "close_l7_augmented",
    "close_l8_imperfect_event",
    "close_l9_imperative_event",
    "close_l10_derivation_family",
    "close_l11_mabni_tool_reference",
    "close_l12_i3rab_relation",
    "gemination_gate",
    "hamza_gate",
    "hamzat_wasl_gate",
    "issue_provisional_certificate",
    "madd_gate",
    "make_closure_certificate",
    "resolve_closure_conflicts",
    "should_block_transition",
    "weak_letter_gate",
]
