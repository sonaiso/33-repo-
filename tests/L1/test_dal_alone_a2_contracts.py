"""
Tests for DAL-A2 dal-alone separation contracts.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.dal_alone_a1 import DAL_A1_FORBIDDEN_OUTPUTS
from taaqqul_slot_geometry.L1.dal_alone_a2 import (
    DAL_A2_ALLOWED_SEPARATION_GATES,
    DAL_A2_FORBIDDEN_OUTPUTS,
    DAL_A2_TRACE_REF,
    DalA2SeparationSurface,
    RawTraceSeparationGate,
    SoundLetterGraphemeSeparationGate,
    UnicodeNormalizationGate,
)
from taaqqul_slot_geometry.L1.domain_ids import DomainID


def _raw_gate_payload() -> dict:
    return {
        "gate_id": "raw-gate-1",
        "raw_trace_ref": "raw-1",
        "separated_trace_kind": "RAW_TRACE_CANDIDATE",
        "evidence_ref": "evidence:raw-gate-1",
        "residuals": frozenset({"RAW_TRACE_NOT_SPEECH"}),
    }


def _unicode_gate_payload() -> dict:
    return {
        "gate_id": "unicode-gate-1",
        "raw_trace_ref": "raw-1",
        "grapheme_candidate_ref": "grapheme-1",
        "normalized_glyph_sequence": ("د",),
        "evidence_ref": "evidence:unicode-gate-1",
    }


def _separation_gate_payload() -> dict:
    return {
        "gate_id": "separation-gate-1",
        "raw_trace_ref": "raw-1",
        "grapheme_candidate_ref": "grapheme-1",
        "letter_carrier_ref": "letter-1",
        "phonetic_realization_ref": "sound-1",
        "atomic_sound_unit_ref": "unit-1",
        "evidence_ref": "evidence:separation-gate-1",
    }


def _surface_payload() -> dict:
    return {
        "surface_id": "a2-surface-1",
        "raw_trace_separation_gate_refs": ("raw-gate-1",),
        "unicode_normalization_gate_refs": ("unicode-gate-1",),
        "sound_letter_grapheme_separation_gate_refs": ("separation-gate-1",),
        "evidence_ref": "evidence:a2-surface-1",
    }


DAL_A2_CASES = (
    (RawTraceSeparationGate, _raw_gate_payload),
    (UnicodeNormalizationGate, _unicode_gate_payload),
    (SoundLetterGraphemeSeparationGate, _separation_gate_payload),
    (DalA2SeparationSurface, _surface_payload),
)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A2_CASES)
def test_dal_a2_entities_are_candidate_only(entity_cls, payload_factory):
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope."""
    entity = entity_cls(**payload_factory())
    assert entity.rank == "CANDIDATE"
    assert entity.trace_ref == DAL_A2_TRACE_REF
    assert entity.domain_id == DomainID.D1_DAL_ONLY


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A2_CASES)
def test_dal_a2_entities_are_frozen(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 3."""
    entity = entity_cls(**payload_factory())
    with pytest.raises(FrozenInstanceError):
        entity.rank = "CERTIFICATE"  # type: ignore[misc]


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A2_CASES)
def test_dal_a2_entities_reject_rank_promotion(entity_cls, payload_factory):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        entity_cls(**payload_factory(), rank="CERTIFICATE")  # type: ignore[arg-type]


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A2_CASES)
def test_dal_a2_entities_require_trace_ref(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2."""
    payload = payload_factory()
    payload["trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A2_CASES)
def test_dal_a2_entities_require_evidence_or_proof_trace(entity_cls, payload_factory):
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope."""
    payload = payload_factory()
    payload["evidence_ref"] = ""
    payload["proof_trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A2_CASES)
def test_dal_a2_entities_reject_non_dal_domain(entity_cls, payload_factory):
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Registry."""
    payload = payload_factory()
    payload["domain_id"] = DomainID.D2_LAFZI_FORM
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


def test_dal_a2_reuses_local_residual_vocabulary_without_global_expansion():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Local Residual Vocabulary."""
    entity = RawTraceSeparationGate(**_raw_gate_payload())
    assert "RAW_TRACE_NOT_SPEECH" in entity.residuals
    assert not hasattr(FailureCode, "RAW_TRACE_NOT_SPEECH")


def test_dal_a2_rejects_non_local_residuals():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Local Residual Vocabulary."""
    payload = _raw_gate_payload()
    payload["residuals"] = frozenset({"GLOBAL_FAILURE_CODE"})
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        RawTraceSeparationGate(**payload)


def test_dal_a2_forbidden_outputs_extend_a1_and_block_closure():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Non-Domain."""
    assert set(DAL_A1_FORBIDDEN_OUTPUTS).issubset(set(DAL_A2_FORBIDDEN_OUTPUTS))
    required = {
        "WordKind",
        "Root",
        "Pattern",
        "LicensedWeight",
        "LexicalMeaning",
        "LafziMadlulGate",
        "DalAloneClosed",
    }
    assert required.issubset(set(DAL_A2_FORBIDDEN_OUTPUTS))


def test_dal_a2_surface_is_not_closure_or_lafzi_gate():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope."""
    surface = DalA2SeparationSurface(**_surface_payload())
    assert surface.separation_status == "DAL_A2_SEPARATION_SURFACE_CANDIDATE"
    assert not hasattr(surface, "closed_state")
    assert not hasattr(surface, "verdict_state")
    assert not hasattr(surface, "lafzi_madlul")
    assert not hasattr(surface, "word_kind")


def test_dal_a2_keeps_a3_outputs_forbidden_not_completed():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path."""
    surface = DalA2SeparationSurface(**_surface_payload())
    assert "ArabicSoundInventory" in surface.forbidden_outputs
    assert "Makhraj" in surface.forbidden_outputs
    assert "Sifah" in surface.forbidden_outputs
    assert "QadihSoundDifference" in surface.forbidden_outputs
    assert not hasattr(surface, "makhraj")
    assert not hasattr(surface, "sifah")
    assert not hasattr(surface, "qadih_sound_difference")


def test_sound_letter_grapheme_separation_rejects_collapsed_refs():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DalAloneClosed condition 1."""
    payload = _separation_gate_payload()
    payload["atomic_sound_unit_ref"] = "sound-1"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        SoundLetterGraphemeSeparationGate(**payload)


def test_dal_a2_allowed_surface_names_are_separation_only():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A2 Scope."""
    assert DAL_A2_ALLOWED_SEPARATION_GATES == (
        "RawTraceSeparationGate",
        "UnicodeNormalizationGate",
        "SoundLetterGraphemeSeparationGate",
        "DalA2SeparationSurface",
    )
    forbidden_fragments = ("Closed", "LafziMadlul", "WordKind", "Meaning")
    assert not any(
        fragment in gate_name
        for gate_name in DAL_A2_ALLOWED_SEPARATION_GATES
        for fragment in forbidden_fragments
    )
