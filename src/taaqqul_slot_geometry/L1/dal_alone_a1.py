"""
DAL-A1 dal-alone carriers and local residual vocabulary.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A1 Scope
Authority: docs/00_MAQOOL_CONSTITUTION.md §5; docs/15_PROJECT_ROADMAP.md §حوكمة التفريع
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.domain_ids import DomainID

Rank = Literal["CANDIDATE"]

DAL_A1_TRACE_REF = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"

DAL_A1_RESIDUAL_CODES: Tuple[str, ...] = (
    "RAW_TRACE_NOT_SPEECH",
    "MAKHRAJ_MISSING",
    "SIFAH_MISSING",
    "QADIH_SOUND_DIFF_MISSING",
    "HARAKA_WITHOUT_CARRIER",
    "MADD_WITHOUT_EXTENSION",
    "SHADDA_UNEXPANDED",
    "HAMZA_UNRESOLVED",
    "SUKUN_COLLISION",
    "SYLLABLE_UNLICENSED",
    "WAQF_UNTESTED",
    "WASL_UNTESTED",
    "UNVOCALIZED_SURFACE",
    "UNUSED_LAFZ",
    "LOAN_PATH_REQUIRED",
    "DELETION_UNLICENSED",
    "ENERGY_COLLISION",
)

DAL_A1_FORBIDDEN_OUTPUTS: Tuple[str, ...] = (
    "WordKind",
    "Root",
    "Pattern",
    "LicensedWeight",
    "LexicalMeaning",
    "VerbalMadlulCandidate",
    "IfadahCandidate",
    "HukmCandidate",
    "TanzilCandidate",
    "Reality",
    "LafziMadlul",
    "DalAloneClosed",
    "LafziMadlulGate",
)

DAL_A1_ALLOWED_CARRIERS: Tuple[str, ...] = (
    "RawTrace",
    "GraphemeCandidate",
    "DalLetterIdentityCarrier",
    "PhoneticRealization",
    "AtomicSoundUnit",
    "DalResidual",
    "DalAloneClosureSurface",
)


def _validate_common(
    *,
    trace_ref: str,
    rank: str,
    domain_id: DomainID,
    forbidden_outputs: Tuple[str, ...],
    evidence_ref: str,
    proof_trace_ref: str,
) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)
    if rank != "CANDIDATE":
        raise ValueError(FailureCode.M_01_16.value)
    if domain_id != DomainID.D1_DAL_ONLY:
        raise ValueError(FailureCode.M_00_22.value)
    if not forbidden_outputs:
        raise ValueError(FailureCode.M_00_22.value)
    if not evidence_ref and not proof_trace_ref:
        raise ValueError(FailureCode.M_00_22.value)


def _validate_local_residuals(residuals: FrozenSet[str]) -> None:
    if not residuals.issubset(frozenset(DAL_A1_RESIDUAL_CODES)):
        raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class RawTrace:
    """Raw trace carrier candidate; it does not decide that the trace is speech."""

    trace_id: str
    raw_trace_ref: str
    trace_kind: str
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A1_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_id or not self.raw_trace_ref or not self.trace_kind:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_local_residuals(self.residuals)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            forbidden_outputs=self.forbidden_outputs,
            evidence_ref=self.evidence_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class GraphemeCandidate:
    """Graphic surface candidate; it is not a final sound realization."""

    grapheme_id: str
    raw_trace_ref: str
    glyph_sequence: Tuple[str, ...]
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A1_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.grapheme_id or not self.raw_trace_ref or not self.glyph_sequence:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_local_residuals(self.residuals)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            forbidden_outputs=self.forbidden_outputs,
            evidence_ref=self.evidence_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class DalLetterIdentityCarrier:
    """Letter identity carrier candidate with no word-kind or meaning output."""

    carrier_id: str
    grapheme_candidate_ref: str
    letter_identity_ref: str
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A1_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.carrier_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.grapheme_candidate_ref or not self.letter_identity_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_local_residuals(self.residuals)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            forbidden_outputs=self.forbidden_outputs,
            evidence_ref=self.evidence_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class PhoneticRealization:
    """Sound realization candidate without makhraj/sifah closure."""

    realization_id: str
    letter_carrier_ref: str
    sound_trace_ref: str
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A1_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.realization_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.letter_carrier_ref or not self.sound_trace_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_local_residuals(self.residuals)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            forbidden_outputs=self.forbidden_outputs,
            evidence_ref=self.evidence_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class AtomicSoundUnit:
    """Atomic sound unit candidate; it is not syllable closure."""

    unit_id: str
    phonetic_realization_ref: str
    sequence_index: int
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A1_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.unit_id or not self.phonetic_realization_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.sequence_index < 0:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_local_residuals(self.residuals)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            forbidden_outputs=self.forbidden_outputs,
            evidence_ref=self.evidence_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class DalResidual:
    """Local residual carrier for dal-alone closure only."""

    residual_id: str
    residual_code: str
    carrier_ref: str
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A1_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.residual_id or not self.carrier_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.residual_code not in DAL_A1_RESIDUAL_CODES:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_local_residuals(self.residuals)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            forbidden_outputs=self.forbidden_outputs,
            evidence_ref=self.evidence_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class DalAloneClosureSurface:
    """Aggregate candidate surface; not DalAloneClosed and not LafziMadlul."""

    surface_id: str
    raw_trace_refs: Tuple[str, ...]
    grapheme_candidate_refs: Tuple[str, ...]
    letter_carrier_refs: Tuple[str, ...]
    phonetic_realization_refs: Tuple[str, ...]
    atomic_sound_unit_refs: Tuple[str, ...]
    dal_residual_refs: Tuple[str, ...]
    closure_status: Literal["DAL_ALONE_CLOSURE_SURFACE_CANDIDATE"] = (
        "DAL_ALONE_CLOSURE_SURFACE_CANDIDATE"
    )
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A1_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.surface_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.raw_trace_refs or not self.grapheme_candidate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.letter_carrier_refs or not self.phonetic_realization_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.atomic_sound_unit_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if self.closure_status != "DAL_ALONE_CLOSURE_SURFACE_CANDIDATE":
            raise ValueError(FailureCode.M_00_22.value)
        _validate_local_residuals(self.residuals)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            forbidden_outputs=self.forbidden_outputs,
            evidence_ref=self.evidence_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


__all__ = [
    "AtomicSoundUnit",
    "DAL_A1_ALLOWED_CARRIERS",
    "DAL_A1_FORBIDDEN_OUTPUTS",
    "DAL_A1_RESIDUAL_CODES",
    "DAL_A1_TRACE_REF",
    "DalAloneClosureSurface",
    "DalLetterIdentityCarrier",
    "DalResidual",
    "GraphemeCandidate",
    "PhoneticRealization",
    "Rank",
    "RawTrace",
]

