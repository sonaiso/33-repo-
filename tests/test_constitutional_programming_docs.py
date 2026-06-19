"""Regression checks for constitutional programming docs (PR-C0)."""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
AMENDMENT_DOC = REPO_ROOT / "docs" / "00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md"
DOMAIN_DOC = REPO_ROOT / "docs" / "05_DOMAIN_REGISTRY_CONSTITUTION.md"
PROOF_DOC = REPO_ROOT / "docs" / "08_PROOF_OBJECT_CONSTITUTION.md"
COVERAGE_DOC = REPO_ROOT / "docs" / "09_COMPUTED_COVERAGE_CONSTITUTION.md"
L1_BOUNDARY_DOC = REPO_ROOT / "docs" / "02_L1_META_LANGUAGE_BOUNDARY.md"


def test_docs_exist_for_constitutional_programming_organization():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5."""
    assert AMENDMENT_DOC.exists()
    assert DOMAIN_DOC.exists()
    assert PROOF_DOC.exists()
    assert COVERAGE_DOC.exists()


def test_rank_remains_candidate_in_l1_programming_kernel():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    content = AMENDMENT_DOC.read_text(encoding="utf-8")
    assert 'rank = "CANDIDATE"' in content


def test_b6_does_not_open_l2():
    """trace_ref: docs/02_L1_META_LANGUAGE_BOUNDARY.md Structural Clarification."""
    content = L1_BOUNDARY_DOC.read_text(encoding="utf-8")
    assert "B6" in content
    assert "does not open L2" in content


def test_manual_coverage_is_forbidden():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    content = COVERAGE_DOC.read_text(encoding="utf-8")
    assert "ComputedVerdict cannot be manually supplied." in content
    assert "Dashboard must be computed." in content
    assert "YAML may declare expected_verdict only." in content
    assert "MRK defaults cannot be all true." in content
