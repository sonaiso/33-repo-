"""
DAL-A2 dal-alone raw/grapheme/letter/sound separation contracts.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope
Authority: docs/00_MAQOOL_CONSTITUTION.md §5; docs/15_PROJECT_ROADMAP.md §حوكمة التفريع
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.dal_alone_a1 import (
    DAL_A1_FORBIDDEN_OUTPUTS,
    DAL_A1_RESIDUAL_CODES,
)
from taaqqul_slot_geometry.L1.domain_ids import DomainID

Rank = Literal["CANDIDATE"]

DAL_A2_TRACE_REF = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"

DAL_A2_FORBIDDEN_OUTPUTS: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS + (
    "ArabicSoundInventory",
    "Makhraj",
    "Sifah",
    "QadihSoundDifference",
)

DAL_A2_ALLOWED_SEPARATION_GATES: Tuple[str, ...] = (
    "RawTraceSeparationGate",
    "UnicodeNormalizationGate",
    "SoundLetterGraphemeSeparationGate",
    "DalA2SeparationSurface",
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
    if not set(DAL_A1_FORBIDDEN_OUTPUTS).issubset(set(forbidden_outputs)):
        raise ValueError(FailureCode.M_00_22.value)
    if set(DAL_A2_FORBIDDEN_OUTPUTS) != set(forbidden_outputs):
        raise ValueError(FailureCode.M_00_22.value)
    if not evidence_ref and not proof_trace_ref:
        raise ValueError(FailureCode.M_00_22.value)


def _validate_local_residuals(residuals: FrozenSet[str]) -> None:
    if not residuals.issubset(frozenset(DAL_A1_RESIDUAL_CODES)):
        raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class RawTraceSeparationGate:
    """Raw trace separation candidate; it does not decide speechhood.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope
    """

    gate_id: str
    raw_trace_ref: str
    separated_trace_kind: Literal["RAW_TRACE_CANDIDATE"]
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A2_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A2_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.gate_id or not self.raw_trace_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.separated_trace_kind != "RAW_TRACE_CANDIDATE":
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
class UnicodeNormalizationGate:
    """Unicode normalization candidate; it does not decide final sound identity.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope
    """

    gate_id: str
    raw_trace_ref: str
    grapheme_candidate_ref: str
    normalized_glyph_sequence: Tuple[str, ...]
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A2_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A2_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.gate_id or not self.raw_trace_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.grapheme_candidate_ref or not self.normalized_glyph_sequence:
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
class SoundLetterGraphemeSeparationGate:
    """Separation candidate for raw trace, grapheme, letter, and sound refs.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope
    """

    gate_id: str
    raw_trace_ref: str
    grapheme_candidate_ref: str
    letter_carrier_ref: str
    phonetic_realization_ref: str
    atomic_sound_unit_ref: str
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A2_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A2_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        refs = (
            self.raw_trace_ref,
            self.grapheme_candidate_ref,
            self.letter_carrier_ref,
            self.phonetic_realization_ref,
            self.atomic_sound_unit_ref,
        )
        if not self.gate_id or not all(refs):
            raise ValueError(FailureCode.M_00_22.value)
        if len(frozenset(refs)) != len(refs):
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
class DalA2SeparationSurface:
    """Aggregate A2 separation candidate; not DalAloneClosed or LafziMadlulGate.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope
    """

    surface_id: str
    raw_trace_separation_gate_refs: Tuple[str, ...]
    unicode_normalization_gate_refs: Tuple[str, ...]
    sound_letter_grapheme_separation_gate_refs: Tuple[str, ...]
    separation_status: Literal["DAL_A2_SEPARATION_SURFACE_CANDIDATE"] = (
        "DAL_A2_SEPARATION_SURFACE_CANDIDATE"
    )
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A2_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A2_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.surface_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.raw_trace_separation_gate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.unicode_normalization_gate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.sound_letter_grapheme_separation_gate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if self.separation_status != "DAL_A2_SEPARATION_SURFACE_CANDIDATE":
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
    "DAL_A2_ALLOWED_SEPARATION_GATES",
    "DAL_A2_FORBIDDEN_OUTPUTS",
    "DAL_A2_TRACE_REF",
    "DalA2SeparationSurface",
    "Rank",
    "RawTraceSeparationGate",
    "SoundLetterGraphemeSeparationGate",
    "UnicodeNormalizationGate",
]
