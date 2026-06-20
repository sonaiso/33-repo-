"""Regression checks for domain vocabulary realignment."""
from pathlib import Path

from tests.markdown_sections import get_section


REPO_ROOT = Path(__file__).parent.parent
DOMAIN_DOC = REPO_ROOT / "docs" / "05_DOMAIN_REGISTRY_CONSTITUTION.md"


def test_d2_lafzi_form_exists():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Canonical L1 Domain IDs."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "D2_LAFZI_FORM" in content


def test_d2_lafzi_madlul_only_removed():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Canonical L1 Domain IDs."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "D2_LAFZI_MADLUL_ONLY" not in content


def test_dal_only_forbids_root_weight_meaning_outputs():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    section = get_section(content, "### D1_DAL_ONLY", "### ")
    assert "Forbidden outputs:" in section
    assert "- root" in section
    assert "- weight" in section
    assert "- meaning" in section


def test_lafzi_form_forbids_lexical_meaning():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    section = get_section(content, "### D2_LAFZI_FORM", "### ")
    assert "Forbidden outputs:" in section
    assert "- lexical meaning" in section


def test_lexical_madlul_forbids_relation_judgment():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    section = get_section(content, "### D3_LEXICAL_MADLUL", "### ")
    assert "Forbidden outputs:" in section
    assert "- final relation verdict" in section
    assert "- hukm" in section


def test_relation_forbids_ifadah_hukm():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    section = get_section(content, "### D4_RELATION", "### ")
    assert "Forbidden outputs:" in section
    assert "- ifadah" in section
    assert "- hukm" in section
