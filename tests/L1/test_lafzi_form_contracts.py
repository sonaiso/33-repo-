"""
Tests for L1 LAFZI_FORM contracts.

Origin: docs/11_LAFZI_FORM_CONSTITUTION.md
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-36
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.domain_ids import DomainID
from taaqqul_slot_geometry.L1.lafzi_form import (
    LAFZI_FORM_FORBIDDEN_OUTPUTS,
    BareQuadriliteralVerbFormCandidate,
    BareTriliteralVerbFormCandidate,
    MabniNounFormCandidate,
    MasdarFormCandidate,
    PatternFormCandidate,
    QuadriliteralJamidFormCandidate,
    RootFormCandidate,
    ToolFormCandidate,
    TriliteralJamidFormCandidate,
    WordFormCandidate,
)


def _root_payload() -> dict:
    return {
        "candidate_id": "root-1",
        "root_form": "كتب",
        "source_surface_ref": "surface-1",
        "proof_object_ref": "proof:root-1",
    }


def _pattern_payload() -> dict:
    return {
        "candidate_id": "pattern-1",
        "pattern_form": "فَعَلَ",
        "source_surface_ref": "surface-1",
        "proof_trace_ref": "trace:pattern-1",
    }


def _word_payload() -> dict:
    return {
        "candidate_id": "word-1",
        "word_form": "كَتَبَ",
        "source_surface_ref": "surface-1",
        "proof_object_ref": "proof:word-1",
    }


def _triliteral_verb_payload() -> dict:
    return {
        "candidate_id": "verb3-1",
        "consonant_skeleton": "كتب",
        "source_surface_ref": "surface-1",
        "proof_object_ref": "proof:verb3-1",
    }


def _quadriliteral_verb_payload() -> dict:
    return {
        "candidate_id": "verb4-1",
        "consonant_skeleton": "دحرج",
        "source_surface_ref": "surface-1",
        "proof_trace_ref": "trace:verb4-1",
    }


def _triliteral_jamid_payload() -> dict:
    return {
        "candidate_id": "jamid3-1",
        "jamid_form": "حجر",
        "source_surface_ref": "surface-1",
        "proof_object_ref": "proof:jamid3-1",
    }


def _quadriliteral_jamid_payload() -> dict:
    return {
        "candidate_id": "jamid4-1",
        "jamid_form": "عقرب",
        "source_surface_ref": "surface-1",
        "proof_trace_ref": "trace:jamid4-1",
    }


def _masdar_payload() -> dict:
    return {
        "candidate_id": "masdar-1",
        "masdar_form": "كِتابة",
        "source_surface_ref": "surface-1",
        "proof_object_ref": "proof:masdar-1",
    }


def _tool_payload() -> dict:
    return {
        "candidate_id": "tool-1",
        "tool_form": "مِفْتاح",
        "source_surface_ref": "surface-1",
        "proof_trace_ref": "trace:tool-1",
    }


def _mabni_payload() -> dict:
    return {
        "candidate_id": "mabni-1",
        "mabni_form": "هذا",
        "source_surface_ref": "surface-1",
        "proof_object_ref": "proof:mabni-1",
    }


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_keep_candidate_rank(entity_cls, payload_factory):
    entity = entity_cls(**payload_factory())
    assert entity.rank == "CANDIDATE"


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_reject_rank_promotion(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        entity_cls(**payload_factory(), rank="CERTIFICATE")  # type: ignore[arg-type]


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_reject_non_lafzi_domain(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), domain_id=DomainID.D3_LEXICAL_MADLUL)


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_reject_non_dal_source_domain(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_09.value):
        entity_cls(**payload_factory(), source_domain_id=DomainID.D2_LAFZI_FORM)


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_require_source_surface(entity_cls, payload_factory):
    payload = payload_factory()
    payload["source_surface_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_require_dal_to_lafzi_bridge(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), required_bridge_ref="OtherBridge")


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_require_proof_ref(entity_cls, payload_factory):
    payload = payload_factory()
    payload["proof_object_ref"] = ""
    payload["proof_trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (RootFormCandidate, _root_payload),
    (PatternFormCandidate, _pattern_payload),
    (WordFormCandidate, _word_payload),
    (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
    (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
    (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    (MasdarFormCandidate, _masdar_payload),
    (ToolFormCandidate, _tool_payload),
    (MabniNounFormCandidate, _mabni_payload),
])
def test_lafzi_entities_require_non_empty_forbidden_outputs(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), forbidden_outputs=())


def test_lafzi_forbidden_outputs_cover_required_semantic_blocks():
    required = {
        "LEXICAL_MEANING",
        "LEXICAL_ROOT",
        "USAGE",
        "RELATION",
        "TOOL_MEANING",
        "MASDAR_MEANING",
        "TRANSITIVITY",
        "ISNAD",
        "IFADAH",
        "HUKM",
        "TANZIL",
    }
    assert required.issubset(set(LAFZI_FORM_FORBIDDEN_OUTPUTS))


def test_root_form_candidate_is_not_lexical_root():
    payload = _root_payload()
    payload["lexical_root_ref"] = "lex:root"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        RootFormCandidate(**payload)


def test_tool_form_candidate_is_not_tool_meaning():
    payload = _tool_payload()
    payload["tool_meaning_ref"] = "meaning:tool"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        ToolFormCandidate(**payload)


def test_masdar_form_candidate_is_not_masdar_meaning():
    payload = _masdar_payload()
    payload["masdar_meaning_ref"] = "meaning:masdar"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        MasdarFormCandidate(**payload)


def test_bare_triliteral_verb_form_rejects_transitivity_or_isnad():
    payload = _triliteral_verb_payload()
    payload["transitivity_profile_ref"] = "transitivity:1"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BareTriliteralVerbFormCandidate(**payload)

    payload = _triliteral_verb_payload()
    payload["isnad_ref"] = "isnad:1"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BareTriliteralVerbFormCandidate(**payload)
