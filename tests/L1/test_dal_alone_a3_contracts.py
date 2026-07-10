"""
Tests for DAL-A3 dal-alone sound inventory contracts.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.dal_alone_a2 import DAL_A2_FORBIDDEN_OUTPUTS
from taaqqul_slot_geometry.L1.dal_alone_a3 import (
    DAL_A3_ALLOWED_SOUND_GATES,
    DAL_A3_FORBIDDEN_OUTPUTS,
    DAL_A3_TRACE_REF,
    ArabicSoundInventoryGate,
    DalA3SoundInventorySurface,
    MakhrajSifahMatrixGate,
    QadihSoundDifferenceGate,
)
from taaqqul_slot_geometry.L1.domain_ids import DomainID


def _inventory_gate_payload() -> dict:
    return {
        "gate_id": "inventory-gate-1",
        "phonetic_realization_refs": ("sound-1",),
        "atomic_sound_unit_refs": ("unit-1",),
        "evidence_ref": "evidence:inventory-gate-1",
        "residuals": frozenset({"MAKHRAJ_MISSING"}),
    }


def _matrix_gate_payload() -> dict:
    return {
        "gate_id": "matrix-gate-1",
        "arabic_sound_inventory_gate_ref": "inventory-gate-1",
        "makhraj_matrix_ref": "matrix:makhraj-1",
        "sifah_matrix_ref": "matrix:sifah-1",
        "evidence_ref": "evidence:matrix-gate-1",
    }


def _qadih_gate_payload() -> dict:
    return {
        "gate_id": "qadih-gate-1",
        "arabic_sound_inventory_gate_ref": "inventory-gate-1",
        "makhraj_sifah_matrix_gate_ref": "matrix-gate-1",
        "contrast_pair_refs": ("pair:dal-thal",),
        "evidence_ref": "evidence:qadih-gate-1",
    }


def _surface_payload() -> dict:
    return {
        "surface_id": "a3-surface-1",
        "arabic_sound_inventory_gate_refs": ("inventory-gate-1",),
        "makhraj_sifah_matrix_gate_refs": ("matrix-gate-1",),
        "qadih_sound_difference_gate_refs": ("qadih-gate-1",),
        "evidence_ref": "evidence:a3-surface-1",
    }


DAL_A3_CASES = (
    (ArabicSoundInventoryGate, _inventory_gate_payload),
    (MakhrajSifahMatrixGate, _matrix_gate_payload),
    (QadihSoundDifferenceGate, _qadih_gate_payload),
    (DalA3SoundInventorySurface, _surface_payload),
)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A3_CASES)
def test_dal_a3_entities_are_candidate_only(entity_cls, payload_factory):
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path."""
    entity = entity_cls(**payload_factory())
    assert entity.rank == "CANDIDATE"
    assert entity.trace_ref == DAL_A3_TRACE_REF
    assert entity.domain_id == DomainID.D1_DAL_ONLY


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A3_CASES)
def test_dal_a3_entities_are_frozen(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 3."""
    entity = entity_cls(**payload_factory())
    with pytest.raises(FrozenInstanceError):
        entity.rank = "CERTIFICATE"  # type: ignore[misc]


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A3_CASES)
def test_dal_a3_entities_reject_rank_promotion(entity_cls, payload_factory):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        entity_cls(**payload_factory(), rank="CERTIFICATE")  # type: ignore[arg-type]


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A3_CASES)
def test_dal_a3_entities_require_trace_ref(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2."""
    payload = payload_factory()
    payload["trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A3_CASES)
def test_dal_a3_entities_require_evidence_or_proof_trace(entity_cls, payload_factory):
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path."""
    payload = payload_factory()
    payload["evidence_ref"] = ""
    payload["proof_trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A3_CASES)
def test_dal_a3_entities_reject_non_dal_domain(entity_cls, payload_factory):
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Registry."""
    payload = payload_factory()
    payload["domain_id"] = DomainID.D2_LAFZI_FORM
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


def test_dal_a3_reuses_local_residual_vocabulary_without_global_expansion():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Local Residual Vocabulary."""
    entity = ArabicSoundInventoryGate(**_inventory_gate_payload())
    assert "MAKHRAJ_MISSING" in entity.residuals
    assert not hasattr(FailureCode, "MAKHRAJ_MISSING")


def test_dal_a3_rejects_non_local_residuals():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Local Residual Vocabulary."""
    payload = _inventory_gate_payload()
    payload["residuals"] = frozenset({"GLOBAL_FAILURE_CODE"})
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        ArabicSoundInventoryGate(**payload)


def test_dal_a3_forbidden_outputs_extend_a2_and_block_closure():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Non-Domain."""
    assert set(DAL_A2_FORBIDDEN_OUTPUTS).issubset(set(DAL_A3_FORBIDDEN_OUTPUTS))
    required = {
        "WordKind",
        "Root",
        "Pattern",
        "LicensedWeight",
        "LexicalMeaning",
        "LafziMadlulGate",
        "DalAloneClosed",
    }
    assert required.issubset(set(DAL_A3_FORBIDDEN_OUTPUTS))


def test_dal_a3_surface_is_not_closure_or_lafzi_gate():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path."""
    surface = DalA3SoundInventorySurface(**_surface_payload())
    assert surface.sound_inventory_status == "DAL_A3_SOUND_INVENTORY_SURFACE_CANDIDATE"
    assert not hasattr(surface, "closed_state")
    assert not hasattr(surface, "verdict_state")
    assert not hasattr(surface, "lafzi_madlul")
    assert not hasattr(surface, "word_kind")


def test_dal_a3_keeps_a4_outputs_forbidden_not_completed():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path."""
    surface = DalA3SoundInventorySurface(**_surface_payload())
    assert "HarakaCarrier" in surface.forbidden_outputs
    assert "MaddExtension" in surface.forbidden_outputs
    assert "HamzaResolution" in surface.forbidden_outputs
    assert "ShaddaIdgham" in surface.forbidden_outputs
    assert "TanwinTrace" in surface.forbidden_outputs
    assert "SukunCollision" in surface.forbidden_outputs
    assert not hasattr(surface, "haraka_carrier")
    assert not hasattr(surface, "madd_extension")
    assert not hasattr(surface, "hamza_resolution")


def test_qadih_gate_rejects_duplicated_contrast_pairs():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DalAloneClosed condition 3."""
    payload = _qadih_gate_payload()
    payload["contrast_pair_refs"] = ("pair:dal-thal", "pair:dal-thal")
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        QadihSoundDifferenceGate(**payload)


def test_matrix_gate_rejects_collapsed_makhraj_sifah_refs():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DalAloneClosed condition 2."""
    payload = _matrix_gate_payload()
    payload["sifah_matrix_ref"] = payload["makhraj_matrix_ref"]
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        MakhrajSifahMatrixGate(**payload)


def test_dal_a3_allowed_surface_names_are_sound_inventory_only():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path."""
    assert DAL_A3_ALLOWED_SOUND_GATES == (
        "ArabicSoundInventoryGate",
        "MakhrajSifahMatrixGate",
        "QadihSoundDifferenceGate",
        "DalA3SoundInventorySurface",
    )
    forbidden_fragments = ("Closed", "LafziMadlul", "WordKind", "Meaning")
    assert not any(
        fragment in gate_name
        for gate_name in DAL_A3_ALLOWED_SOUND_GATES
        for fragment in forbidden_fragments
    )
