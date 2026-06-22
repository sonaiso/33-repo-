"""
L1 signifier domain contracts (DAL internal ordering).

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (L1 open)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

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

_TRACE_REF = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"


def _validate_common(trace_ref: str, rank: str, trace: Tuple[str, ...]) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)
    if rank != "CANDIDATE":
        raise ValueError(FailureCode.M_01_16.value)
    if not trace:
        raise ValueError(FailureCode.M_00_22.value)


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
    "MotionDomainCertificate",
    "MotionFunction",
    "MotionState",
    "PauseEffect",
    "SIGNIFIER_DOMAIN_ORDER",
    "SignifierDomain",
    "WaqfWaslDomainCertificate",
]
