"""Regression checks for the D2_LAFZI_FORM contract document."""
from pathlib import Path

from tests.markdown_sections import get_section


REPO_ROOT = Path(__file__).parent.parent
LAFZI_CONTRACT_DOC = REPO_ROOT / "docs" / "11_LAFZI_FORM_CONTRACT.md"


def test_lafzi_contract_doc_exists():
    """trace_ref: docs/11_LAFZI_FORM_CONTRACT.md DomainID."""
    assert LAFZI_CONTRACT_DOC.exists()


def test_domain_id_is_d2_lafzi_form():
    """trace_ref: docs/11_LAFZI_FORM_CONTRACT.md DomainID."""
    content = LAFZI_CONTRACT_DOC.read_text(encoding="utf-8")
    section = get_section(content, "## DomainID", "## ")
    assert "D2_LAFZI_FORM" in section


def test_contract_declares_required_headers():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Required Contract Headers Per Domain."""
    content = LAFZI_CONTRACT_DOC.read_text(encoding="utf-8")
    required_headers = (
        "## DomainID",
        "## SharedOrigin",
        "## DomainOrigin",
        "## MRK requirements",
        "## Branch types",
        "## Layer contracts",
        "## Element contracts",
        "## Allowed operations",
        "## Forbidden outputs",
        "## Required exit bridge",
        "## Failure codes",
        "## Residual policy",
    )
    for header in required_headers:
        assert header in content


def test_forbidden_outputs_match_domain_registry():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = LAFZI_CONTRACT_DOC.read_text(encoding="utf-8")
    section = get_section(content, "## Forbidden outputs", "## ")
    assert "- lexical meaning" in section
    assert "- lexical usage" in section
    assert "- relation" in section
    assert "- ifadah" in section
    assert "- hukm" in section


def test_required_exit_bridge_requires_lexical_proof():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Cross-Domain Restrictions."""
    content = LAFZI_CONTRACT_DOC.read_text(encoding="utf-8")
    section = get_section(content, "## Required exit bridge", "## ")
    assert "LafziToLexicalBridge" in section
    assert "LexicalProof" in section
