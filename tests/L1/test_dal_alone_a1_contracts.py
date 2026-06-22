"""
Tests for DAL-A1 dal-alone carrier contracts.

Origin: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A1 Scope
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.dal_alone_a1 import (
    DAL_A1_ALLOWED_CARRIERS,
    DAL_A1_FORBIDDEN_OUTPUTS,
    DAL_A1_RESIDUAL_CODES,
    DAL_A1_TRACE_REF,
    AtomicSoundUnit,
    DalAloneClosureSurface,
    DalLetterIdentityCarrier,
    DalResidual,
    GraphemeCandidate,
    PhoneticRealization,
    RawTrace,
)
from taaqqul_slot_geometry.L1.domain_ids import DomainID


def _raw_trace_payload() -> dict:
    return {
        "trace_id": "raw-1",
        "raw_trace_ref": "trace:raw-1",
        "trace_kind": "graphic_trace",
        "evidence_ref": "evidence:raw-1",
    }


def _grapheme_payload() -> dict:
    return {
        "grapheme_id": "grapheme-1",
        "raw_trace_ref": "raw-1",
        "glyph_sequence": ("د",),
        "evidence_ref": "evidence:grapheme-1",
    }


def _letter_payload() -> dict:
    return {
        "carrier_id": "letter-1",
        "grapheme_candidate_ref": "grapheme-1",
        "letter_identity_ref": "letter:DAL",
        "evidence_ref": "evidence:letter-1",
    }


def _phonetic_payload() -> dict:
    return {
        "realization_id": "sound-1",
        "letter_carrier_ref": "letter-1",
        "sound_trace_ref": "sound:dal-1",
        "evidence_ref": "evidence:sound-1",
    }


def _sound_unit_payload() -> dict:
    return {
        "unit_id": "unit-1",
        "phonetic_realization_ref": "sound-1",
        "sequence_index": 0,
        "evidence_ref": "evidence:unit-1",
    }


def _residual_payload() -> dict:
    return {
        "residual_id": "residual-1",
        "residual_code": "MAKHRAJ_MISSING",
        "carrier_ref": "unit-1",
        "evidence_ref": "evidence:residual-1",
        "residuals": frozenset({"MAKHRAJ_MISSING"}),
    }


def _surface_payload() -> dict:
    return {
        "surface_id": "surface-1",
        "raw_trace_refs": ("raw-1",),
        "grapheme_candidate_refs": ("grapheme-1",),
        "letter_carrier_refs": ("letter-1",),
        "phonetic_realization_refs": ("sound-1",),
        "atomic_sound_unit_refs": ("unit-1",),
        "dal_residual_refs": ("residual-1",),
        "evidence_ref": "evidence:surface-1",
        "residuals": frozenset({"MAKHRAJ_MISSING"}),
    }


DAL_A1_CASES = (
    (RawTrace, _raw_trace_payload),
    (GraphemeCandidate, _grapheme_payload),
    (DalLetterIdentityCarrier, _letter_payload),
    (PhoneticRealization, _phonetic_payload),
    (AtomicSoundUnit, _sound_unit_payload),
    (DalResidual, _residual_payload),
    (DalAloneClosureSurface, _surface_payload),
)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A1_CASES)
def test_dal_a1_entities_are_candidate_only(entity_cls, payload_factory):
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A1 Scope."""
    entity = entity_cls(**payload_factory())
    assert entity.rank == "CANDIDATE"
    assert entity.trace_ref == DAL_A1_TRACE_REF
    assert entity.domain_id == DomainID.D1_DAL_ONLY


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A1_CASES)
def test_dal_a1_entities_are_frozen(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 3."""
    entity = entity_cls(**payload_factory())
    with pytest.raises(FrozenInstanceError):
        entity.rank = "CERTIFICATE"  # type: ignore[misc]


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A1_CASES)
def test_dal_a1_entities_reject_rank_promotion(entity_cls, payload_factory):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        entity_cls(**payload_factory(), rank="CERTIFICATE")  # type: ignore[arg-type]


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A1_CASES)
def test_dal_a1_entities_require_trace_ref(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2."""
    payload = payload_factory()
    payload["trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", DAL_A1_CASES)
def test_dal_a1_entities_require_evidence_or_proof_trace(entity_cls, payload_factory):
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A1 Scope."""
    payload = payload_factory()
    payload["evidence_ref"] = ""
    payload["proof_trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


def test_dal_a1_residual_vocabulary_is_local_and_complete():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Local Residual Vocabulary."""
    expected = {
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
    }
    assert expected == set(DAL_A1_RESIDUAL_CODES)
    assert all(not hasattr(FailureCode, code) for code in expected)


def test_dal_a1_rejects_non_local_residuals():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Local Residual Vocabulary."""
    payload = _raw_trace_payload()
    payload["residuals"] = frozenset({"GLOBAL_FAILURE_CODE"})
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        RawTrace(**payload)


def test_dal_a1_forbidden_outputs_block_meaning_and_lafzi_crossing():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Non-Domain."""
    expected = {
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
    }
    assert expected.issubset(set(DAL_A1_FORBIDDEN_OUTPUTS))


def test_dal_a1_surface_is_not_dal_alone_closed():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A1 Scope."""
    surface = DalAloneClosureSurface(**_surface_payload())
    assert surface.closure_status == "DAL_ALONE_CLOSURE_SURFACE_CANDIDATE"
    assert surface.closure_status != "DalAloneClosed"


def test_dal_a1_allowed_carriers_do_not_define_gates_or_bridges():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A1 Scope."""
    assert DAL_A1_ALLOWED_CARRIERS == (
        "RawTrace",
        "GraphemeCandidate",
        "DalLetterIdentityCarrier",
        "PhoneticRealization",
        "AtomicSoundUnit",
        "DalResidual",
        "DalAloneClosureSurface",
    )
    forbidden_fragments = ("Gate", "Bridge", "Meaning", "WordKind")
    assert not any(
        fragment in carrier
        for carrier in DAL_A1_ALLOWED_CARRIERS
        for fragment in forbidden_fragments
    )

