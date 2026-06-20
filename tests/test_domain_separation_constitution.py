"""Regression checks for domain separation constitution rules."""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
DOMAIN_DOC = REPO_ROOT / "docs" / "05_DOMAIN_REGISTRY_CONSTITUTION.md"
AMENDMENT_DOC = REPO_ROOT / "docs" / "00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md"


def test_no_candidate_without_domain():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Separation Law."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "No candidate without domain." in content


def test_no_direct_dalonly_to_lexicalmadlul():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Cross-Domain Restrictions."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "No direct DalOnly → LexicalMadlul." in content


def test_lafziform_requires_lexicalproof_for_lexicalmadlul():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Cross-Domain Restrictions."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "No LafziForm → LexicalMadlul without LexicalProof." in content


def test_lexicalmadlul_requires_relationbridge_for_relation():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Cross-Domain Restrictions."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "No LexicalMadlul → Relation without RelationBridge." in content


def test_no_contract_without_domain_exists_in_amendment():
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md Constitutional Programming Axiom."""
    content = AMENDMENT_DOC.read_text(encoding="utf-8")
    assert "No contract without domain." in content
