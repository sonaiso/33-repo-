"""Regression checks for proof object constitutional requirements."""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
PROOF_DOC = REPO_ROOT / "docs" / "08_PROOF_OBJECT_CONSTITUTION.md"
AMENDMENT_DOC = REPO_ROOT / "docs" / "00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md"


def test_no_boolean_as_proof():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    content = PROOF_DOC.read_text(encoding="utf-8")
    assert "No Boolean as proof." in content


def test_required_proof_objects_present():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    content = PROOF_DOC.read_text(encoding="utf-8")
    assert "MRKProof is required." in content
    assert "IdentityProof is required." in content
    assert "GateProof is required." in content
    assert "BridgeProof is required." in content
    assert "DomainProof is required." in content
    assert "EvidenceProof is required." in content
    assert "CoverageProof is required." in content


def test_rank_ceiling_and_certificate_forbidden_in_l1():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    content = AMENDMENT_DOC.read_text(encoding="utf-8")
    assert 'rank = "CANDIDATE"' in content
    assert "No rank promotion." in content
    assert "Certificate is forbidden in L1 programming kernel." in content


def test_trace_and_evidence_chain_is_enforced():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    content = PROOF_DOC.read_text(encoding="utf-8")
    assert "No ProofObject without trace." in content
    assert "No Trace without evidence." in content
