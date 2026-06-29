"""Tests for Aqd audit-only L1 contracts.

Origin: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md
"""
from __future__ import annotations

from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.aqd_audit_contracts import (
    AQD_FORBIDDEN_OUTPUTS,
    AQD_TRACE_REF,
    AqdAttributeContract,
    AqdAuditResult,
    AqdInflectionAuditContract,
    AqdMorphologicalBranchContract,
    AqdPartialBranchContract,
    AqdRelationTripletContract,
    AqdReverseAuditContract,
    AqdTemporalBindingContract,
    AqdUniversalContract,
    audit_aqd_contract_shape,
)

REPO_ROOT = Path(__file__).parent.parent.parent


def _universal_payload() -> dict:
    return {
        "contract_id": "aqd-universal-1",
        "universal_scope_ref": "scope:aqd",
        "obligation_ref": "obligation:proof-bearing-contract",
        "proof_object_ref": "proof:aqd-universal-1",
    }


def _partial_branch_payload() -> dict:
    return {
        "contract_id": "aqd-partial-branch-1",
        "origin_ref": "origin:licensed",
        "branch_ref": "branch:partial",
        "relation_with_prev_ref": "relation:prev-candidate",
        "relation_with_next_ref": "relation:next-candidate",
        "relation_next_to_prev_ref": "relation:next-to-prev-candidate",
        "condition_ref": "condition:required",
        "sabab_ref": "sabab:required",
        "preventer_ref": "preventer:checked",
        "proof_trace_ref": "trace:aqd-partial-branch-1",
    }


def _attribute_payload() -> dict:
    return {
        "contract_id": "aqd-attribute-1",
        "carrier_ref": "carrier:zaid",
        "attribute_ref": "attribute:walking-candidate",
        "relation_effect_candidate_ref": "effect:licensed-relation-candidate",
        "proof_object_ref": "proof:aqd-attribute-1",
    }


def _relation_triplet_payload() -> dict:
    return {
        "contract_id": "aqd-relation-triplet-1",
        "previous_relation_ref": "relation:previous-candidate",
        "next_relation_ref": "relation:next-candidate",
        "next_to_previous_relation_ref": "relation:next-to-previous-candidate",
        "relation_function_candidate_ref": "candidate:relation-function",
        "tool_surface_ref": "tool:surface-only",
        "license_condition_ref": "license:bridge-proof-required",
        "proof_object_ref": "proof:aqd-relation-triplet-1",
    }


def _temporal_binding_payload() -> dict:
    return {
        "contract_id": "aqd-temporal-binding-1",
        "temporal_scope_ref": "temporal:scope",
        "utterance_time_ref": "time:utterance",
        "attribute_time_ref": "time:attribute",
        "temporal_policy_ref": "policy:temporal-audit-only",
        "proof_object_ref": "proof:aqd-temporal-binding-1",
    }


def _inflection_payload() -> dict:
    return {
        "contract_id": "aqd-inflection-1",
        "operator_ref": "operator:amil-candidate",
        "carrier_ref": "carrier:inflectable",
        "temporal_binding_ref": "temporal:binding-candidate",
        "effect_candidate_ref": "effect:irab-candidate",
        "inflection_policy_ref": "policy:licensed-effect-only",
        "proof_object_ref": "proof:aqd-inflection-1",
    }


def _morphological_branch_payload() -> dict:
    return {
        "contract_id": "aqd-morph-branch-1",
        "surface_weight_ref": "weight:surface-witness",
        "licensed_origin_ref": "origin:licensed",
        "branch_ref": "branch:morphological-candidate",
        "path_card_ref": "path-card:required",
        "masdar_open_ref": "masdar-open:required",
        "residual_policy_ref": "policy:residual",
        "proof_object_ref": "proof:aqd-morph-branch-1",
    }


def _reverse_audit_payload() -> dict:
    return {
        "contract_id": "aqd-reverse-1",
        "source_stage_ref": "stage:s13",
        "target_stage_ref": "stage:s0",
        "reverse_policy_ref": "policy:reverse-audit-only",
        "proof_trace_ref": "trace:aqd-reverse-1",
    }


AQD_CONTRACT_CASES = (
    (AqdUniversalContract, _universal_payload),
    (AqdPartialBranchContract, _partial_branch_payload),
    (AqdAttributeContract, _attribute_payload),
    (AqdRelationTripletContract, _relation_triplet_payload),
    (AqdTemporalBindingContract, _temporal_binding_payload),
    (AqdInflectionAuditContract, _inflection_payload),
    (AqdMorphologicalBranchContract, _morphological_branch_payload),
    (AqdReverseAuditContract, _reverse_audit_payload),
)


def test_all_contract_dataclasses_are_frozen():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 3."""
    for entity_cls, payload_factory in AQD_CONTRACT_CASES:
        assert is_dataclass(entity_cls)
        entity = entity_cls(**payload_factory())
        with pytest.raises(FrozenInstanceError):
            entity.rank = "CERTIFICATE"  # type: ignore[misc]


@pytest.mark.parametrize("entity_cls,payload_factory", AQD_CONTRACT_CASES)
def test_rank_promotion_is_rejected(entity_cls, payload_factory):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md."""
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        entity_cls(**payload_factory(), rank="CERTIFICATE")


@pytest.mark.parametrize("entity_cls,payload_factory", AQD_CONTRACT_CASES)
def test_authoritative_true_is_rejected(entity_cls, payload_factory):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md."""
    with pytest.raises(ValueError, match=FailureCode.M_CX_02.value):
        entity_cls(**payload_factory(), authoritative=True)


@pytest.mark.parametrize("entity_cls,payload_factory", AQD_CONTRACT_CASES)
def test_runtime_authorized_true_is_rejected(entity_cls, payload_factory):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md."""
    with pytest.raises(ValueError, match=FailureCode.M_CX_02.value):
        entity_cls(**payload_factory(), runtime_authorized=True)


@pytest.mark.parametrize("entity_cls,payload_factory", AQD_CONTRACT_CASES)
def test_missing_trace_ref_is_rejected(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2."""
    with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
        entity_cls(**payload_factory(), trace_ref="")


@pytest.mark.parametrize("entity_cls,payload_factory", AQD_CONTRACT_CASES)
def test_missing_proof_refs_are_rejected(entity_cls, payload_factory):
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md."""
    payload = payload_factory()
    payload["proof_object_ref"] = ""
    payload["proof_trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", AQD_CONTRACT_CASES)
def test_missing_forbidden_outputs_are_rejected(entity_cls, payload_factory):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload_factory(), forbidden_outputs=())


def test_forbidden_outputs_include_required_runtime_blocks():
    """trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md."""
    required = {
        "RUNTIME_RESULT",
        "AUTHORITATIVE_DECISION",
        "FINAL_MEANING",
        "RELATION_RUNTIME",
        "IFADAH_RUNTIME",
        "HUKM",
        "TANZIL",
        "YAQIN",
        "KERNEL_DECISION",
    }
    assert required == set(AQD_FORBIDDEN_OUTPUTS)


def test_partial_branch_contract_requires_all_branch_guard_refs():
    """trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md."""
    required_fields = (
        "origin_ref",
        "branch_ref",
        "relation_with_prev_ref",
        "relation_with_next_ref",
        "relation_next_to_prev_ref",
        "condition_ref",
        "sabab_ref",
        "preventer_ref",
    )
    for field_name in required_fields:
        payload = _partial_branch_payload()
        payload[field_name] = ""
        with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
            AqdPartialBranchContract(**payload)


def test_temporal_binding_validates_shape_only_without_time_execution():
    """trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md."""
    contract = AqdTemporalBindingContract(**_temporal_binding_payload())
    result = audit_aqd_contract_shape(contract)

    assert result.shape_valid is True
    assert result.runtime_authorized is False
    assert result.authoritative is False
    assert result.status == "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED"
    assert not hasattr(contract, "execute_time")
    assert not hasattr(contract, "time_result")


def test_inflection_contract_does_not_produce_final_irab_or_meaning():
    """trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md."""
    contract = AqdInflectionAuditContract(**_inflection_payload())

    assert contract.effect_candidate_ref == "effect:irab-candidate"
    assert "FINAL_MEANING" in contract.forbidden_outputs
    assert not hasattr(contract, "final_irab")
    assert not hasattr(contract, "final_meaning")
    assert not hasattr(contract, "lexical_meaning")


def test_reverse_audit_requires_stage_refs_without_reverse_execution():
    """trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md."""
    for field_name in ("source_stage_ref", "target_stage_ref"):
        payload = _reverse_audit_payload()
        payload[field_name] = ""
        with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
            AqdReverseAuditContract(**payload)

    contract = AqdReverseAuditContract(**_reverse_audit_payload())
    result = audit_aqd_contract_shape(contract)
    assert result.status == "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED"
    assert result.runtime_authorized is False
    assert not hasattr(contract, "execute_reverse")
    assert not hasattr(contract, "reverse_result")


def test_aqd_audit_result_for_valid_shape_keeps_runtime_blocked():
    """trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md."""
    result = audit_aqd_contract_shape(AqdUniversalContract(**_universal_payload()))

    assert isinstance(result, AqdAuditResult)
    assert result.shape_valid is True
    assert result.runtime_authorized is False
    assert result.authoritative is False
    assert result.trace_ref == AQD_TRACE_REF
    assert result.rank == "CANDIDATE"


def test_invalid_aqd_shape_remains_blocked():
    """trace_ref: docs/22_AQD_AUDIT_CONTRACTS_CONSTITUTION.md."""
    result = audit_aqd_contract_shape(object())

    assert result.shape_valid is False
    assert result.runtime_authorized is False
    assert result.status == "AUDIT_SHAPE_INVALID_RUNTIME_STILL_BLOCKED"
    assert "AQD_CONTRACT_SHAPE_INVALID" in result.residuals


def test_no_parser_runtime_or_kernel_files_are_created():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md."""
    forbidden_paths = (
        "src/taaqqul_slot_geometry/L1/aqd_parser.py",
        "src/taaqqul_slot_geometry/L1/aqd_interpreter.py",
        "src/taaqqul_slot_geometry/L1/binding_kernel.py",
        "src/taaqqul_slot_geometry/L1/decision_engine.py",
        "coverage_matrix_v0.1.yaml",
    )

    for path in forbidden_paths:
        assert not (REPO_ROOT / path).exists()
