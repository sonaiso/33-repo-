"""Regression checks for agent binding constitutional restrictions."""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
AGENT_DOC = REPO_ROOT / "docs" / "00B_AGENT_BINDING_CONSTITUTION.md"
AMENDMENT_DOC = REPO_ROOT / "docs" / "00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md"


def test_agent_is_proposer_not_judge():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Principle."""
    content = AGENT_DOC.read_text(encoding="utf-8")
    assert "Agent proposes." in content
    assert "Kernel verifies." in content
    assert "Constitution governs." in content


def test_agent_cannot_grant_core_authorities():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Non-Delegable Kernel Powers."""
    content = AGENT_DOC.read_text(encoding="utf-8")
    assert "The agent may not grant MRK." in content
    assert "The agent may not grant Bridge." in content
    assert "The agent may not raise rank." in content
    assert "The agent may not close Coverage." in content


def test_missing_proof_must_block():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Non-Delegable Kernel Powers."""
    content = AGENT_DOC.read_text(encoding="utf-8")
    assert "BLOCKED_MISSING_PROOF" in content


def test_no_agent_output_without_kernel_verdict():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md Constitutional Programming Axiom."""
    content = AMENDMENT_DOC.read_text(encoding="utf-8")
    assert "No agent output without Kernel verdict." in content
