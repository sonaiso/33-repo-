"""
Tests for L1 operation/gate/bridge specs.

Origin: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-34
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.domain_bridge_gate import BridgeSpec, GateSpec, OperationSpec
from taaqqul_slot_geometry.L1.domain_ids import DomainID


def _operation_payload() -> dict:
    return {
        "operation_id": "op-lafzi-1",
        "source_domain_id": DomainID.D2_LAFZI_FORM,
        "target_domain_id": DomainID.D2_LAFZI_FORM,
        "operation_kind": "lafzi_form_classification",
        "input_contract_refs": ("docs/11_LAFZI_FORM_CONTRACT.md",),
        "output_contract_refs": ("docs/11_LAFZI_FORM_CONTRACT.md",),
        "forbidden_outputs": ("lexical meaning",),
        "required_gate_ids": ("gate-lafzi-1",),
        "trace_ref": "docs/06_DOMAIN_SLOT_GEOMETRY_CONSTITUTION.md",
    }


def _gate_payload() -> dict:
    return {
        "gate_id": "gate-lafzi-1",
        "source_domain_id": DomainID.D2_LAFZI_FORM,
        "input_contract_ref": "docs/11_LAFZI_FORM_CONTRACT.md",
        "predicate_ref": "predicates/lafzi_form_gate.py:is_allowed",
        "failure_code": FailureCode.M_CX_04,
        "residual_code": "gate_needs_more_context",
        "forbidden_outputs": ("lexical meaning",),
        "trace_ref": "docs/07_GATE_BRIDGE_CONSTITUTION.md",
    }


def _bridge_payload() -> dict:
    return {
        "bridge_id": "bridge-lafzi-to-lexical",
        "source_domain_id": DomainID.D2_LAFZI_FORM,
        "target_domain_id": DomainID.D3_LEXICAL_MADLUL,
        "source_contract_ref": "docs/11_LAFZI_FORM_CONTRACT.md",
        "target_contract_ref": "docs/05_DOMAIN_REGISTRY_CONSTITUTION.md ### D3_LEXICAL_MADLUL",
        "translator_ref": "bridges/lafzi_to_lexical.py:translate",
        "invariant_policy_ref": "policies/identity_preservation.md#lafzi_to_lexical",
        "required_proof_kinds": ("IdentityProof", "BridgeProof"),
        "forbidden_outputs": ("relation", "ifadah", "hukm"),
        "trace_ref": "docs/07_GATE_BRIDGE_CONSTITUTION.md",
    }


def test_operation_spec_keeps_rank_candidate():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    spec = OperationSpec(**_operation_payload())
    assert spec.rank == "CANDIDATE"


def test_gate_spec_requires_predicate_ref():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law."""
    payload = _gate_payload()
    payload["predicate_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        GateSpec(**payload)


def test_gate_spec_keeps_rank_candidate():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    spec = GateSpec(**_gate_payload())
    assert spec.rank == "CANDIDATE"


def test_gate_spec_rejects_non_failure_code_enum():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5."""
    payload = _gate_payload()
    payload["failure_code"] = "M_CX_04"
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        GateSpec(**payload)  # type: ignore[arg-type]


def test_bridge_spec_requires_translator_ref():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law."""
    payload = _bridge_payload()
    payload["translator_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BridgeSpec(**payload)


def test_bridge_spec_requires_invariant_policy_ref():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law."""
    payload = _bridge_payload()
    payload["invariant_policy_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BridgeSpec(**payload)


def test_bridge_spec_rejects_same_source_and_target_domain():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law."""
    payload = _bridge_payload()
    payload["target_domain_id"] = DomainID.D2_LAFZI_FORM
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BridgeSpec(**payload)


def test_bridge_spec_keeps_rank_candidate():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    spec = BridgeSpec(**_bridge_payload())
    assert spec.rank == "CANDIDATE"


@pytest.mark.parametrize("spec_cls,payload", [
    (OperationSpec, _operation_payload),
    (GateSpec, _gate_payload),
    (BridgeSpec, _bridge_payload),
])
def test_specs_reject_rank_promotion(spec_cls, payload):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        spec_cls(**payload(), rank="CERTIFICATE")  # type: ignore[arg-type]
