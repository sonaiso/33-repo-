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
    FORM_CONTRACT_STAGE,
    FORM_ONLY_STATUS,
    LAFZI_FORM_FORBIDDEN_OUTPUTS,
    NO_ADDITION,
    SOURCE_CONTRACT_REF,
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
from taaqqul_slot_geometry.core.rank import Rank


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


ALL_ENTITIES = [
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
]


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_keep_candidate_rank(entity_cls, payload_factory):
    entity = entity_cls(**payload_factory())
    assert entity.rank == "CANDIDATE"


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_accept_explicit_candidate_string_rank(entity_cls, payload_factory):
    entity = entity_cls(**payload_factory(), rank="CANDIDATE")
    assert entity.rank == "CANDIDATE"


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_accept_rank_enum_as_string_subtype(entity_cls, payload_factory):
    entity = entity_cls(**payload_factory(), rank=Rank.CANDIDATE)
    assert entity.rank == "CANDIDATE"


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_reject_rank_promotion(entity_cls, payload_factory):
    for invalid_rank in ("", "INVALID", "CERTIFIED", "Rank.CANDIDATE", "Rank.CERTIFIED", "Rank.REJECTED", None):
        with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
            entity_cls(**payload_factory(), rank=invalid_rank)  # type: ignore[arg-type]


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_reject_non_lafzi_domain(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), domain_id=DomainID.D3_LEXICAL_MADLUL)


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_reject_non_dal_source_domain(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_09.value):
        entity_cls(**payload_factory(), source_domain_id=DomainID.D2_LAFZI_FORM)


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_require_source_surface(entity_cls, payload_factory):
    payload = payload_factory()
    payload["source_surface_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_require_source_contract_ref(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), source_contract_ref="OtherSurface")


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_require_dal_to_lafzi_bridge(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), required_bridge_ref="OtherBridge")


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_require_proof_ref(entity_cls, payload_factory):
    payload = payload_factory()
    payload["proof_object_ref"] = ""
    payload["proof_trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_require_non_empty_forbidden_outputs(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), forbidden_outputs=())


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
def test_lafzi_entities_require_lafzi_c2_stage_and_form_only_status(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), form_contract_stage="LAFZI_C1")
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), form_only_status="NOT_FORM_ONLY")

    entity = entity_cls(**payload_factory())
    assert entity.form_contract_stage == FORM_CONTRACT_STAGE
    assert entity.form_only_status == FORM_ONLY_STATUS
    assert entity.source_contract_ref == SOURCE_CONTRACT_REF


def test_lafzi_entities_reject_missing_required_forbidden_output():
    payload = _word_payload()
    reduced = tuple(item for item in LAFZI_FORM_FORBIDDEN_OUTPUTS if item != "HUKM")
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        WordFormCandidate(**payload, forbidden_outputs=reduced)


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
    assert set(LAFZI_FORM_FORBIDDEN_OUTPUTS) == required


def test_bare_triliteral_verb_rejects_non_triliteral_arity():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BareTriliteralVerbFormCandidate(**_triliteral_verb_payload(), arity=4)


def test_bare_quadriliteral_verb_rejects_non_quadriliteral_arity():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BareQuadriliteralVerbFormCandidate(**_quadriliteral_verb_payload(), arity=3)


def test_triliteral_jamid_rejects_non_triliteral_arity():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        TriliteralJamidFormCandidate(**_triliteral_jamid_payload(), arity=4)


def test_quadriliteral_jamid_rejects_non_quadriliteral_arity():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        QuadriliteralJamidFormCandidate(**_quadriliteral_jamid_payload(), arity=3)


def test_root_rejects_out_of_contract_arity():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        RootFormCandidate(**_root_payload(), arity=2)


@pytest.mark.parametrize(
    "entity_cls,payload_factory",
    [
        (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
        (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
        (TriliteralJamidFormCandidate, _triliteral_jamid_payload),
        (QuadriliteralJamidFormCandidate, _quadriliteral_jamid_payload),
    ],
)
def test_bare_and_jamid_candidates_require_no_addition(entity_cls, payload_factory):
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), addition_status="WITH_ADDITION")

    entity = entity_cls(**payload_factory())
    assert entity.addition_status == NO_ADDITION


def test_root_form_candidate_is_not_lexical_root():
    payload = _root_payload()
    payload["lexical_root_ref"] = "lex:root"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        RootFormCandidate(**payload)


def test_pattern_form_candidate_is_not_lexical_meaning():
    payload = _pattern_payload()
    payload["lexical_meaning_ref"] = "lex:meaning"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        PatternFormCandidate(**payload)


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


@pytest.mark.parametrize(
    "entity_cls,payload_factory",
    [
        (BareTriliteralVerbFormCandidate, _triliteral_verb_payload),
        (BareQuadriliteralVerbFormCandidate, _quadriliteral_verb_payload),
    ],
)
def test_bare_verb_form_candidates_reject_transitivity_or_isnad(entity_cls, payload_factory):
    payload = payload_factory()
    payload["transitivity_profile_ref"] = "transitivity:1"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)

    payload = payload_factory()
    payload["isnad_ref"] = "isnad:1"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", ALL_ENTITIES)
@pytest.mark.parametrize(
    "leak_field",
    [
        "relation_ref",
        "ifadah_ref",
        "hukm_ref",
        "tanzil_ref",
        "usage_ref",
        "lexical_entry_ref",
    ],
)
def test_lafzi_entities_do_not_accept_relational_or_runtime_leak_fields(entity_cls, payload_factory, leak_field):
    payload = payload_factory()
    payload[leak_field] = "leak:value"
    with pytest.raises(TypeError):
        entity_cls(**payload)
