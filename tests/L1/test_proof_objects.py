"""
Tests for L1 proof object stubs.

Origin: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-33
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1 import proof_objects
from taaqqul_slot_geometry.L1.proof_objects import (
    BridgeProof,
    CoverageProof,
    DomainProof,
    EvidenceProof,
    GateProof,
    IdentityProof,
    MRKProof,
    ProofTrace,
)


def _trace() -> ProofTrace:
    return ProofTrace(
        trace_id="trace-1",
        trace_ref="docs/08_PROOF_OBJECT_CONSTITUTION.md",
        steps=("step-1",),
        evidence_refs=("ev-1",),
    )


def _base() -> dict:
    return {
        "proof_id": "proof-1",
        "proof_kind": "stub",
        "domain_id": "D2_LAFZI_FORM",
        "checked_gate_ids": ("gate-1",),
        "checked_bridge_ids": ("bridge-1",),
        "preserved_identity_refs": ("id-1",),
        "forbidden_outputs_checked": ("lexical meaning",),
        "evidence_refs": ("ev-1",),
        "residual_codes": (),
        "failure_codes": (),
        "trace": _trace(),
        "trace_ref": "docs/08_PROOF_OBJECT_CONSTITUTION.md",
    }


def test_no_rank_above_candidate():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        MRKProof(**_base(), rank="CERTIFICATE")  # type: ignore[arg-type]


def test_proof_object_requires_trace_ref():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    payload = _base()
    payload["trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
        MRKProof(**payload)


def test_identity_proof_rejects_identity_loss():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7."""
    with pytest.raises(ValueError, match=FailureCode.M_CX_01.value):
        IdentityProof(**_base(), lost_identity_refs=("id-missing",))


def test_gate_proof_requires_gate_id():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        GateProof(**_base())


def test_bridge_proof_requires_source_and_target_domains():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BridgeProof(**_base(), bridge_id="lafzi-lexical")


def test_evidence_proof_requires_scope():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        EvidenceProof(**_base())


def test_trace_requires_evidence_refs():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    with pytest.raises(TypeError):
        ProofTrace(
            trace_id="trace-1",
            trace_ref="docs/08_PROOF_OBJECT_CONSTITUTION.md",
            steps=("step-1",),
        )


def test_trace_rejects_explicit_empty_evidence_refs():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        ProofTrace(
            trace_id="trace-1",
            trace_ref="docs/08_PROOF_OBJECT_CONSTITUTION.md",
            steps=("step-1",),
            evidence_refs=(),
        )


def test_trace_accepts_evidence_refs():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    trace = _trace()
    assert trace.evidence_refs == ("ev-1",)


def test_evidence_proof_requires_invalidators():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        EvidenceProof(**_base(), evidence_scope=("domain",))


def test_evidence_proof_rejects_explicit_empty_invalidators():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        EvidenceProof(
            **_base(),
            evidence_scope=("domain",),
            invalidators_checked=(),
        )


def test_evidence_proof_requires_residual_indicator():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    payload = _base()
    payload["residual_codes"] = ()
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        EvidenceProof(
            **payload,
            evidence_scope=("domain",),
            invalidators_checked=("inv-1",),
            residuals=frozenset(),
        )


def test_coverage_proof_requires_positive_negative_residual_cases():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        CoverageProof(**_base())


def test_no_certificate_symbol_exported():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    assert "CERTIFICATE" not in proof_objects.__dict__


def test_boolean_is_not_accepted_as_proof():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Forbidden substitutions, including identity_preserved: bool."""
    assert not hasattr(MRKProof, "domain_proved")
    assert not hasattr(MRKProof, "gate_passed")
    assert not hasattr(IdentityProof, "identity_preserved")
    assert not hasattr(IdentityProof, "is_preserved")


def test_domain_proof_requires_contract_ref():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md."""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        DomainProof(**_base())
