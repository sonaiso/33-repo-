"""
DAL-A3 dal-alone Arabic sound inventory and makhraj/sifah/qadih contracts.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path
Authority: docs/00_MAQOOL_CONSTITUTION.md §5; docs/15_PROJECT_ROADMAP.md §حوكمة التفريع
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.dal_alone_a1 import DAL_A1_RESIDUAL_CODES
from taaqqul_slot_geometry.L1.dal_alone_a2 import DAL_A2_FORBIDDEN_OUTPUTS
from taaqqul_slot_geometry.L1.domain_ids import DomainID

Rank = Literal["CANDIDATE"]

DAL_A3_TRACE_REF = "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"

DAL_A3_FORBIDDEN_OUTPUTS: Tuple[str, ...] = DAL_A2_FORBIDDEN_OUTPUTS + (
    "HarakaCarrier",
    "MaddExtension",
    "HamzaResolution",
    "ShaddaIdgham",
    "TanwinTrace",
    "SukunCollision",
)

DAL_A3_ALLOWED_SOUND_GATES: Tuple[str, ...] = (
    "ArabicSoundInventoryGate",
    "MakhrajSifahMatrixGate",
    "QadihSoundDifferenceGate",
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
class ArabicSoundInventoryGate:
    """Arabic sound inventory candidate; no closure and no lafzi crossing."""

    gate_id: str
    phonetic_realization_refs: Tuple[str, ...]
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
        if not self.gate_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.phonetic_realization_refs or not self.atomic_sound_unit_refs:
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
class MakhrajSifahMatrixGate:
    """Makhraj/sifah matrix candidate over the A3 inventory surface."""

    gate_id: str
    arabic_sound_inventory_gate_ref: str
    makhraj_matrix_ref: str
    sifah_matrix_ref: str
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
        if not self.gate_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.arabic_sound_inventory_gate_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.makhraj_matrix_ref or not self.sifah_matrix_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if self.makhraj_matrix_ref == self.sifah_matrix_ref:
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
class QadihSoundDifferenceGate:
    """Qadih sound-difference candidate over licensed A3 inventory/matrix refs."""

    gate_id: str
    arabic_sound_inventory_gate_ref: str
    makhraj_sifah_matrix_gate_ref: str
    contrast_pair_refs: Tuple[str, ...]
    qadih_status: Literal["QADIH_SOUND_DIFFERENCE_CANDIDATE"] = (
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
        if not self.gate_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.arabic_sound_inventory_gate_ref or not self.makhraj_sifah_matrix_gate_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.contrast_pair_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if len(frozenset(self.contrast_pair_refs)) != len(self.contrast_pair_refs):
            raise ValueError(FailureCode.M_00_22.value)
        if self.qadih_status != "QADIH_SOUND_DIFFERENCE_CANDIDATE":
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
    """Aggregate A3 candidate surface; not closure and not lafzi gate."""

    surface_id: str
    arabic_sound_inventory_gate_refs: Tuple[str, ...]
    makhraj_sifah_matrix_gate_refs: Tuple[str, ...]
    qadih_sound_difference_gate_refs: Tuple[str, ...]
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
        if not self.surface_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.arabic_sound_inventory_gate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.makhraj_sifah_matrix_gate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.qadih_sound_difference_gate_refs:
            raise ValueError(FailureCode.M_00_22.value)
        if self.sound_inventory_status != "DAL_A3_SOUND_INVENTORY_SURFACE_CANDIDATE":
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
    "ArabicSoundInventoryGate",
    "DAL_A3_ALLOWED_SOUND_GATES",
    "DAL_A3_FORBIDDEN_OUTPUTS",
    "DAL_A3_TRACE_REF",
    "DalA3SoundInventorySurface",
    "MakhrajSifahMatrixGate",
    "QadihSoundDifferenceGate",
    "Rank",
]
