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
_ALLOWED_EVENT_PATTERNS = frozenset({"فَعَلَ", "فَعِلَ", "فَعُلَ"})
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
) -> ClosureCertificate:
    trace_recorded = bool(trace.trace_id)
    residuals_audited = True
    next_layer_permission = bool(next_permissions)
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


def close_l6_past_mujarrad_event(
    *,
    pattern: str,
    has_fa_il_slot: bool,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = ()
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
    minimal_mujarrad_closed: bool,
    trace: Trace,
) -> ClosureCertificate:
    residual_entries: Tuple[Residual, ...] = ()
    if not minimal_mujarrad_closed:
        residual_entries += (
            Residual(
                family="path",
                severity="blocker",
                message="augmentation_before_mujarrad",
                remediation_hint="close L4/L6 before opening augmented path",
            )
        ,)
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


__all__ = [
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
    "close_l6_past_mujarrad_event",
    "close_l7_augmented",
    "gemination_gate",
    "hamza_gate",
    "hamzat_wasl_gate",
    "issue_provisional_certificate",
    "madd_gate",
    "make_closure_certificate",
    "should_block_transition",
    "weak_letter_gate",
]
