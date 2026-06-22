"""
DAL-A3 dal-alone Arabic sound inventory candidate contracts.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
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

DAL_A3_TRACE_REF = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"

DAL_A3_FORBIDDEN_OUTPUTS: Tuple[str, ...] = DAL_A1_FORBIDDEN_OUTPUTS + (
    "ArabicSoundInventoryClosed",
    "MakhrajClosed",
    "SifahClosed",
    "QadihSoundDifferenceClosed",
    "FinalArabicSoundInventory",
    "FinalMakhraj",
    "FinalSifah",
    "FinalQadihSoundDifference",
    "SoundVerdict",
    "SoundClosure",
)

DAL_A3_ALLOWED_INVENTORY_CONTRACTS: Tuple[str, ...] = (
    "ArabicSoundInventoryCandidate",
    "MakhrajCandidate",
    "SifahCandidate",
    "QadihSoundDifferenceCandidate",
    "MakhrajSifahMatrixCandidate",
    "DalA3SoundInventorySurface",
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
    if set(DAL_A3_FORBIDDEN_OUTPUTS) != set(forbidden_outputs):
        raise ValueError(FailureCode.M_00_22.value)
    if not evidence_ref and not proof_trace_ref:
        raise ValueError(FailureCode.M_00_22.value)


def _validate_local_residuals(residuals: FrozenSet[str]) -> None:
    if not residuals.issubset(frozenset(DAL_A1_RESIDUAL_CODES)):
        raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class ArabicSoundInventoryCandidate:
    """Arabic sound inventory candidate derived from A2 separation.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
    """

    inventory_id: str
    dal_a2_surface_ref: str
    atomic_sound_unit_refs: Tuple[str, ...]
    inventory_status: Literal["ARABIC_SOUND_INVENTORY_CANDIDATE"] = (
        "ARABIC_SOUND_INVENTORY_CANDIDATE"
    )
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A3_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A3_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.inventory_id or not self.dal_a2_surface_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.atomic_sound_unit_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if self.inventory_status != "ARABIC_SOUND_INVENTORY_CANDIDATE":
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
class MakhrajCandidate:
    """Makhraj visibility candidate; not a final makhraj verdict.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
    """

    makhraj_id: str
    dal_a2_surface_ref: str
    atomic_sound_unit_ref: str
    makhraj_ref: str
    makhraj_status: Literal["MAKHRAJ_CANDIDATE"] = "MAKHRAJ_CANDIDATE"
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A3_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A3_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.makhraj_id or not self.dal_a2_surface_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.atomic_sound_unit_ref or not self.makhraj_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.makhraj_status != "MAKHRAJ_CANDIDATE":
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
class SifahCandidate:
    """Sifah visibility candidate; not a final sifah verdict.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
    """

    sifah_id: str
    dal_a2_surface_ref: str
    atomic_sound_unit_ref: str
    sifah_refs: Tuple[str, ...]
    sifah_status: Literal["SIFAH_CANDIDATE"] = "SIFAH_CANDIDATE"
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A3_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A3_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.sifah_id or not self.dal_a2_surface_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.atomic_sound_unit_ref or not self.sifah_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if self.sifah_status != "SIFAH_CANDIDATE":
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
class QadihSoundDifferenceCandidate:
    """Qadih sound-difference visibility candidate.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
    """

    difference_id: str
    dal_a2_surface_ref: str
    source_atomic_sound_unit_ref: str
    target_atomic_sound_unit_ref: str
    qadih_difference_ref: str
    difference_status: Literal["QADIH_SOUND_DIFFERENCE_CANDIDATE"] = (
        "QADIH_SOUND_DIFFERENCE_CANDIDATE"
    )
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A3_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A3_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.difference_id or not self.dal_a2_surface_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.source_atomic_sound_unit_ref or not self.target_atomic_sound_unit_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.source_atomic_sound_unit_ref == self.target_atomic_sound_unit_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.qadih_difference_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.difference_status != "QADIH_SOUND_DIFFERENCE_CANDIDATE":
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
class MakhrajSifahMatrixCandidate:
    """Candidate matrix joining makhraj, sifah, and qadih visibility refs.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
    """

    matrix_id: str
    dal_a2_surface_ref: str
    makhraj_candidate_refs: Tuple[str, ...]
    sifah_candidate_refs: Tuple[str, ...]
    qadih_sound_difference_candidate_refs: Tuple[str, ...]
    matrix_status: Literal["MAKHRAJ_SIFAH_MATRIX_CANDIDATE"] = (
        "MAKHRAJ_SIFAH_MATRIX_CANDIDATE"
    )
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A3_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A3_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.matrix_id or not self.dal_a2_surface_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.makhraj_candidate_refs or not self.sifah_candidate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.qadih_sound_difference_candidate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if self.matrix_status != "MAKHRAJ_SIFAH_MATRIX_CANDIDATE":
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
class DalA3SoundInventorySurface:
    """Aggregate A3 sound inventory candidate; not DalAloneClosed.

    trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
    """

    surface_id: str
    dal_a2_surface_ref: str
    arabic_sound_inventory_candidate_refs: Tuple[str, ...]
    makhraj_sifah_matrix_candidate_refs: Tuple[str, ...]
    sound_inventory_status: Literal["DAL_A3_SOUND_INVENTORY_SURFACE_CANDIDATE"] = (
        "DAL_A3_SOUND_INVENTORY_SURFACE_CANDIDATE"
    )
    evidence_ref: str = ""
    proof_trace_ref: str = ""
    domain_id: DomainID = DomainID.D1_DAL_ONLY
    forbidden_outputs: Tuple[str, ...] = DAL_A3_FORBIDDEN_OUTPUTS
    trace_ref: str = DAL_A3_TRACE_REF
    rank: Rank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.surface_id or not self.dal_a2_surface_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.arabic_sound_inventory_candidate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.makhraj_sifah_matrix_candidate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if (
            self.sound_inventory_status
            != "DAL_A3_SOUND_INVENTORY_SURFACE_CANDIDATE"
        ):
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
    "ArabicSoundInventoryCandidate",
    "DAL_A3_ALLOWED_INVENTORY_CONTRACTS",
    "DAL_A3_FORBIDDEN_OUTPUTS",
    "DAL_A3_TRACE_REF",
    "DalA3SoundInventorySurface",
    "MakhrajCandidate",
    "MakhrajSifahMatrixCandidate",
    "QadihSoundDifferenceCandidate",
    "Rank",
    "SifahCandidate",
]
