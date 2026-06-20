"""Regression checks for domain vocabulary realignment."""
from pathlib import Path


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
    assert "### D1_DAL_ONLY" in content
    assert "- root" in content
    assert "- weight" in content
    assert "- meaning" in content


def test_lafzi_form_forbids_lexical_meaning():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "### D2_LAFZI_FORM" in content
    assert "- lexical meaning" in content


def test_lexical_madlul_forbids_relation_judgment():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "### D3_LEXICAL_MADLUL" in content
    assert "- final relation verdict" in content
    assert "- hukm" in content


def test_relation_forbids_ifadah_hukm():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Domain Vocabulary Contracts."""
    content = DOMAIN_DOC.read_text(encoding="utf-8")
    assert "### D4_RELATION" in content
    assert "- ifadah" in content
    assert "- hukm" in content
