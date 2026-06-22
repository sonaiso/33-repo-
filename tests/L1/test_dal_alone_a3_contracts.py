"""
Tests for DAL-A3 dal-alone Arabic sound inventory candidate contracts.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.dal_alone_a1 import DAL_A1_FORBIDDEN_OUTPUTS
from taaqqul_slot_geometry.L1.dal_alone_a2 import DAL_A2_FORBIDDEN_OUTPUTS
from taaqqul_slot_geometry.L1.dal_alone_a3 import (
    DAL_A3_ALLOWED_INVENTORY_CONTRACTS,
    DAL_A3_FORBIDDEN_OUTPUTS,
    DAL_A3_TRACE_REF,
    ArabicSoundInventoryCandidate,
    DalA3SoundInventorySurface,
    MakhrajCandidate,
    MakhrajSifahMatrixCandidate,
    QadihSoundDifferenceCandidate,
    SifahCandidate,
)
from taaqqul_slot_geometry.L1.domain_ids import DomainID


def _inventory_payload() -> dict:
    return {
        "inventory_id": "inventory-1",
        "dal_a2_surface_ref": "a2-surface-1",
        "atomic_sound_unit_refs": ("unit-1", "unit-2"),
        "evidence_ref": "evidence:inventory-1",
        "residuals": frozenset({"MAKHRAJ_MISSING"}),
    }


def _makhraj_payload() -> dict:
    return {
        "makhraj_id": "makhraj-1",
        "dal_a2_surface_ref": "a2-surface-1",
        "atomic_sound_unit_ref": "unit-1",
        "makhraj_ref": "makhraj:dental",
        "evidence_ref": "evidence:makhraj-1",
    }


def _sifah_payload() -> dict:
    return {
        "sifah_id": "sifah-1",
        "dal_a2_surface_ref": "a2-surface-1",
        "atomic_sound_unit_ref": "unit-1",
        "sifah_refs": ("sifah:jahr",),
        "evidence_ref": "evidence:sifah-1",
    }


def _qadih_payload() -> dict:
    return {
        "difference_id": "qadih-1",
        "dal_a2_surface_ref": "a2-surface-1",
        "source_atomic_sound_unit_ref": "unit-1",
        "target_atomic_sound_unit_ref": "unit-2",
        "qadih_difference_ref": "qadih:unit-1-unit-2",
        "evidence_ref": "evidence:qadih-1",
    }


def _matrix_payload() -> dict:
    return {
        "matrix_id": "matrix-1",
        "dal_a2_surface_ref": "a2-surface-1",
        "makhraj_candidate_refs": ("makhraj-1",),
        "sifah_candidate_refs": ("sifah-1",),
        "qadih_sound_difference_candidate_refs": ("qadih-1",),
        "evidence_ref": "evidence:matrix-1",
    }


def _surface_payload() -> dict:
    return {
        "surface_id": "a3-surface-1",
        "dal_a2_surface_ref": "a2-surface-1",
        "arabic_sound_inventory_candidate_refs": ("inventory-1",),
        "makhraj_sifah_matrix_candidate_refs": ("matrix-1",),
        "evidence_ref": "evidence:a3-surface-1",
    }


DAL_A3_CASES = (
    (ArabicSoundInventoryCandidate, _inventory_payload),
    (MakhrajCandidate, _makhraj_payload),
    (SifahCandidate, _sifah_payload),
    (QadihSoundDifferenceCandidate, _qadih_payload),
    (MakhrajSifahMatrixCandidate, _matrix_payload),
    (DalA3SoundInventorySurface, _surface_payload),
)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A3_CASES)
def test_dal_a3_entities_are_candidate_only(entity_cls, payload_factory):
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope."""
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
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope."""
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
    entity = ArabicSoundInventoryCandidate(**_inventory_payload())
    assert "MAKHRAJ_MISSING" in entity.residuals
    assert not hasattr(FailureCode, "MAKHRAJ_MISSING")


def test_dal_a3_rejects_non_local_residuals():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Local Residual Vocabulary."""
    payload = _inventory_payload()
    payload["residuals"] = frozenset({"GLOBAL_FAILURE_CODE"})
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        ArabicSoundInventoryCandidate(**payload)


def test_dal_a3_forbidden_outputs_preserve_non_domain_boundaries():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Non-Domain."""
    assert set(DAL_A1_FORBIDDEN_OUTPUTS).issubset(set(DAL_A3_FORBIDDEN_OUTPUTS))
    required = {
        "WordKind",
        "Root",
        "Pattern",
        "LicensedWeight",
        "LexicalMeaning",
        "LafziMadlulGate",
        "DalAloneClosed",
        "FinalArabicSoundInventory",
        "FinalMakhraj",
        "FinalSifah",
        "FinalQadihSoundDifference",
        "SoundClosure",
    }
    assert required.issubset(set(DAL_A3_FORBIDDEN_OUTPUTS))


def test_dal_a2_still_forbids_a3_outputs():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope."""
    assert "ArabicSoundInventory" in DAL_A2_FORBIDDEN_OUTPUTS
    assert "Makhraj" in DAL_A2_FORBIDDEN_OUTPUTS
    assert "Sifah" in DAL_A2_FORBIDDEN_OUTPUTS
    assert "QadihSoundDifference" in DAL_A2_FORBIDDEN_OUTPUTS


def test_dal_a3_surface_is_not_dal_alone_closed_or_lafzi_gate():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope."""
    surface = DalA3SoundInventorySurface(**_surface_payload())
    assert surface.sound_inventory_status == "DAL_A3_SOUND_INVENTORY_SURFACE_CANDIDATE"
    assert not hasattr(surface, "closed_state")
    assert not hasattr(surface, "verdict_state")
    assert not hasattr(surface, "lafzi_madlul")
    assert not hasattr(surface, "word_kind")
    assert not hasattr(surface, "meaning")


def test_dal_a3_candidates_do_not_produce_final_sound_closure():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope."""
    inventory = ArabicSoundInventoryCandidate(**_inventory_payload())
    makhraj = MakhrajCandidate(**_makhraj_payload())
    sifah = SifahCandidate(**_sifah_payload())
    assert inventory.inventory_status == "ARABIC_SOUND_INVENTORY_CANDIDATE"
    assert makhraj.makhraj_status == "MAKHRAJ_CANDIDATE"
    assert sifah.sifah_status == "SIFAH_CANDIDATE"
    assert not hasattr(inventory, "final_inventory")
    assert not hasattr(makhraj, "final_makhraj")
    assert not hasattr(sifah, "final_sifah")


def test_qadih_sound_difference_rejects_collapsed_refs():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DalAloneClosed condition 3."""
    collapsed_payload = _qadih_payload()
    collapsed_payload["target_atomic_sound_unit_ref"] = "unit-1"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        QadihSoundDifferenceCandidate(**collapsed_payload)


def test_dal_a3_allowed_contract_names_are_candidate_only():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A3 Scope."""
    assert DAL_A3_ALLOWED_INVENTORY_CONTRACTS == (
        "ArabicSoundInventoryCandidate",
        "MakhrajCandidate",
        "SifahCandidate",
        "QadihSoundDifferenceCandidate",
        "MakhrajSifahMatrixCandidate",
        "DalA3SoundInventorySurface",
    )
    forbidden_fragments = ("Closed", "LafziMadlul", "WordKind", "Meaning")
    assert not any(
        fragment in contract_name
        for contract_name in DAL_A3_ALLOWED_INVENTORY_CONTRACTS
        for fragment in forbidden_fragments
    )
