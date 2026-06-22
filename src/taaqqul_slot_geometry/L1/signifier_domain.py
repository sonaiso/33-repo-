"""
L1 signifier domain contracts (DAL internal ordering).

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (L1 open)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple, cast

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode

Rank = Literal["CANDIDATE"]
SignifierDomain = Literal[
    "trace",
    "letter",
    "motion",
    "phonetic_atom",
    "syllable",
    "waqf_wasl",
    "additive_letter",
    "root_stem",
    "minimal_mujarrad",
    "weight",
    "jamid_anchor",
    "event_path",
    "mabni_tool",
    "reference",
    "proper_name",
    "loanword",
    "irab_ready",
]

SIGNIFIER_DOMAIN_ORDER: Tuple[SignifierDomain, ...] = (
    "trace",
    "letter",
    "motion",
    "phonetic_atom",
    "syllable",
    "waqf_wasl",
    "additive_letter",
    "root_stem",
    "minimal_mujarrad",
    "weight",
    "jamid_anchor",
    "event_path",
    "mabni_tool",
    "reference",
    "proper_name",
    "loanword",
    "irab_ready",
)

MotionState = Literal[
    "FATHA",
    "DAMMA",
    "KASRA",
    "SUKUN",
    "MADD",
    "SHADDA",
    "TANWIN",
]
MotionFunction = Literal[
    "opening",
    "closure",
    "extension",
    "compression",
    "nominal_ending",
    "case",
    "weight",
    "wasl_waqf",
]
AdditiveFunction = Literal[
    "mudari_prefix",
    "hamzat_ziyadah",
    "ifti3al_ta",
    "tafa3ul_ta",
    "mufa3alah_alif",
    "infi3al_nun",
    "istif3al_sin_ta",
    "nisbah_ya",
    "ta_nith_alif",
    "plural_waw",
    "dual_alif",
    "niswah_nun",
    "extra_letter_candidate",
]
PauseEffect = Literal["none", "drop_motion", "incidental_sukun", "freeze_ending"]
ConnectionEffect = Literal["none", "restore_motion", "require_hamzat_wasl", "resolve_two_sukuns"]
ClosureType = Literal["nominal_closure", "eventual_open", "functional_closure", "undetermined"]
DomainLicenseStatus = Literal["closed", "provisional", "blocked"]
DomainBlockReason = Literal[
    "none",
    "blocked_origin_missing",
    "blocked_domain_without_sabab",
    "blocked_by_mani",
    "blocked_origin_not_closed",
]
ManiSeverity = Literal["warning", "blocker"]

SIGNIFIER_DOMAIN_TRANSITIONS: dict[SignifierDomain, Tuple[SignifierDomain, ...]] = {
    "trace": ("letter",),
    "letter": ("motion",),
    "motion": ("phonetic_atom",),
    "phonetic_atom": ("syllable",),
    "syllable": ("waqf_wasl", "root_stem"),
    "waqf_wasl": ("root_stem",),
    "additive_letter": ("irab_ready",),
    "root_stem": ("minimal_mujarrad", "proper_name", "loanword"),
    "minimal_mujarrad": ("weight",),
    "weight": ("jamid_anchor", "event_path"),
    "jamid_anchor": ("irab_ready",),
    "event_path": ("additive_letter", "irab_ready"),
    "mabni_tool": ("reference", "irab_ready"),
    "reference": ("irab_ready",),
    "proper_name": ("irab_ready",),
    "loanword": ("irab_ready",),
    "irab_ready": tuple(),
}
INDEPENDENT_ENTRY_DOMAINS: Tuple[SignifierDomain, ...] = ("trace", "mabni_tool")

_TRACE_REF = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"


def _validate_common(trace_ref: str, rank: str, trace: Tuple[str, ...]) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)
    if rank != "CANDIDATE":
        raise ValueError(FailureCode.M_01_16.value)
    if not trace:
        raise ValueError(FailureCode.M_00_22.value)


def previous_signifier_domains(domain: SignifierDomain) -> Tuple[SignifierDomain, ...]:
    """Return predecessor domains derived from the transition registry."""
    if domain in INDEPENDENT_ENTRY_DOMAINS:
        return tuple()
    predecessors = tuple(
        candidate_domain
        for candidate_domain, next_domains in SIGNIFIER_DOMAIN_TRANSITIONS.items()
        if domain in next_domains
    )
    return predecessors


def previous_signifier_domain(domain: SignifierDomain) -> SignifierDomain | None:
    """Return single predecessor only when graph predecessor is unambiguous."""
    predecessors = previous_signifier_domains(domain)
    if len(predecessors) != 1:
        return None
    return cast(SignifierDomain, predecessors[0])


def next_signifier_domains(domain: SignifierDomain) -> Tuple[SignifierDomain, ...]:
    """Return licensed next domains from the transition registry for a domain."""
    return SIGNIFIER_DOMAIN_TRANSITIONS.get(domain, tuple())


@dataclass(frozen=True)
class ManiCheck:
    residual_code: str
    severity: ManiSeverity
    trace: Tuple[str, ...]
    trace_ref: str = _TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.residual_code:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(self.trace_ref, self.rank, self.trace)


@dataclass(frozen=True)
class DomainRelation:
    domain: SignifierDomain
    previous_domains: Tuple[SignifierDomain, ...]
    next_domains: Tuple[SignifierDomain, ...]
    relation_to_previous: Tuple[str, ...]
    relation_to_next: Tuple[str, ...]
    relation_previous_to_next: Tuple[str, ...]
    trace: Tuple[str, ...]
    trace_ref: str = _TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        expected_previous = previous_signifier_domains(self.domain)
        expected_next = next_signifier_domains(self.domain)
        if self.previous_domains != expected_previous:
            raise ValueError(FailureCode.M_CX_04.value)
        if self.next_domains != expected_next:
            raise ValueError(FailureCode.M_CX_04.value)
        if not self.relation_to_previous:
            raise ValueError(FailureCode.M_00_22.value)
        if expected_next and not self.relation_to_next:
            raise ValueError(FailureCode.M_00_22.value)
        if len(self.relation_to_next) != len(self.next_domains):
            raise ValueError(FailureCode.M_CX_01.value)
        if not self.previous_domains:
            expected_previous_to_next_count = len(self.next_domains)
        else:
            expected_previous_to_next_count = len(self.previous_domains) * len(self.next_domains)
        if len(self.relation_previous_to_next) != expected_previous_to_next_count:
            raise ValueError(FailureCode.M_CX_01.value)
        _validate_common(self.trace_ref, self.rank, self.trace)


@dataclass(frozen=True)
class DomainCertificate:
    domain: SignifierDomain
    origin_certificate: str
    sabab: str
    mani_residuals: Tuple[ManiCheck, ...]
    boundary_declared: bool
    relation: DomainRelation
    trace: Tuple[str, ...]
    status: DomainLicenseStatus
    status_reason: DomainBlockReason
    allowed_next_domains: Tuple[SignifierDomain, ...]
    origin_status: DomainLicenseStatus = "closed"
    trace_ref: str = _TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.domain != self.relation.domain:
            raise ValueError(FailureCode.M_CX_01.value)
        if not self.boundary_declared:
            raise ValueError(FailureCode.M_00_22.value)
        if self.status != "blocked":
            if not self.origin_certificate.strip():
                raise ValueError(FailureCode.M_00_22.value)
            if not self.sabab.strip():
                raise ValueError(FailureCode.M_00_22.value)
        if self.status == "blocked" and self.allowed_next_domains:
            raise ValueError(FailureCode.M_CX_04.value)
        if self.status != "blocked" and self.allowed_next_domains != self.relation.next_domains:
            raise ValueError(FailureCode.M_CX_04.value)
        if self.status == "blocked" and self.status_reason == "none":
            raise ValueError(FailureCode.M_CX_04.value)
        if self.status != "blocked" and self.status_reason != "none":
            raise ValueError(FailureCode.M_CX_04.value)
        _validate_common(self.trace_ref, self.rank, self.trace)


def domain_relation(domain: SignifierDomain, trace: Tuple[str, ...]) -> DomainRelation:
    """Construct previous/next and previous→next relation contracts for one domain."""
    previous_domains = previous_signifier_domains(domain)
    next_domains = next_signifier_domains(domain)
    if not previous_domains:
        relation_to_previous = ("entry_point_for_signifier_domains",)
    else:
        relation_to_previous = tuple(
            f"opens_after_{previous_domain}_closure" for previous_domain in previous_domains
        )
    relation_to_next = tuple(f"licenses_{next_domain}_inspection" for next_domain in next_domains)
    if not previous_domains:
        relation_previous_to_next = tuple(f"trace_to_{next_domain}_via_{domain}" for next_domain in next_domains)
    else:
        relation_previous_to_next = tuple(
            f"{previous_domain}_to_{next_domain}_via_{domain}"
            for previous_domain in previous_domains
            for next_domain in next_domains
        )
    return DomainRelation(
        domain=domain,
        previous_domains=previous_domains,
        next_domains=next_domains,
        relation_to_previous=relation_to_previous,
        relation_to_next=relation_to_next,
        relation_previous_to_next=relation_previous_to_next,
        trace=trace,
    )


def license_domain(
    domain: SignifierDomain,
    origin_certificate: str,
    sabab: str,
    mani_checks: Tuple[ManiCheck, ...],
    trace: Tuple[str, ...],
    *,
    boundary_declared: bool = True,
    origin_status: DomainLicenseStatus = "closed",
) -> DomainCertificate:
    """Issue a domain certificate after origin/sabab/mani and closure-state checks."""
    relation = domain_relation(domain=domain, trace=trace)
    status: DomainLicenseStatus = "closed"
    status_reason: DomainBlockReason = "none"
    if not origin_certificate.strip():
        status = "blocked"
        status_reason = "blocked_origin_missing"
    elif not sabab.strip():
        status = "blocked"
        status_reason = "blocked_domain_without_sabab"
    elif origin_status != "closed":
        status = "blocked"
        status_reason = "blocked_origin_not_closed"
    elif any(check.severity == "blocker" for check in mani_checks):
        status = "blocked"
        status_reason = "blocked_by_mani"
    elif mani_checks:
        status = "provisional"

    allowed_next_domains: Tuple[SignifierDomain, ...] = tuple()
    if status in {"closed", "provisional"}:
        allowed_next_domains = relation.next_domains

    return DomainCertificate(
        domain=domain,
        origin_certificate=origin_certificate,
        sabab=sabab,
        mani_residuals=mani_checks,
        boundary_declared=boundary_declared,
        relation=relation,
        trace=trace,
        status=status,
        status_reason=status_reason,
        allowed_next_domains=allowed_next_domains,
        origin_status=origin_status,
    )


@dataclass(frozen=True)
class MotionDomainCertificate:
    carrier_letter: str
    motion_state: MotionState
    function: MotionFunction
    trace: Tuple[str, ...]
    domain: SignifierDomain = "motion"
    trace_ref: str = _TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.carrier_letter:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain != "motion":
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(self.trace_ref, self.rank, self.trace)


@dataclass(frozen=True)
class AdditiveLetterDomainCertificate:
    candidate_letter: str
    position: int
    additive_function: AdditiveFunction
    required_origin_certificate: str
    blocked_until_mujarrad_closure: bool
    trace: Tuple[str, ...]
    domain: SignifierDomain = "additive_letter"
    trace_ref: str = _TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_letter:
            raise ValueError(FailureCode.M_00_22.value)
        if self.position < 0:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.required_origin_certificate:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.blocked_until_mujarrad_closure:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain != "additive_letter":
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(self.trace_ref, self.rank, self.trace)


@dataclass(frozen=True)
class WaqfWaslDomainCertificate:
    unit: str
    can_pause: bool
    must_connect: bool
    pause_effect: PauseEffect
    connection_effect: ConnectionEffect
    closure_type: ClosureType
    trace: Tuple[str, ...]
    domain: SignifierDomain = "waqf_wasl"
    trace_ref: str = _TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.unit:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.can_pause and not self.must_connect:
            raise ValueError(FailureCode.M_00_22.value)
        if self.domain != "waqf_wasl":
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(self.trace_ref, self.rank, self.trace)


__all__ = [
    "AdditiveFunction",
    "AdditiveLetterDomainCertificate",
    "ClosureType",
    "ConnectionEffect",
    "DomainBlockReason",
    "DomainCertificate",
    "DomainLicenseStatus",
    "DomainRelation",
    "ManiCheck",
    "MotionDomainCertificate",
    "MotionFunction",
    "MotionState",
    "PauseEffect",
    "SIGNIFIER_DOMAIN_ORDER",
    "SIGNIFIER_DOMAIN_TRANSITIONS",
    "INDEPENDENT_ENTRY_DOMAINS",
    "SignifierDomain",
    "WaqfWaslDomainCertificate",
    "domain_relation",
    "license_domain",
    "next_signifier_domains",
    "previous_signifier_domains",
    "previous_signifier_domain",
]
