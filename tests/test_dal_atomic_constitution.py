"""Regression checks for DAL atomic constitution constraints."""
from pathlib import Path

from tests.markdown_sections import get_section


REPO_ROOT = Path(__file__).parent.parent
DAL_ATOMIC_DOC = REPO_ROOT / "docs" / "10_DAL_ATOMIC_CONSTITUTION.md"


def test_dal_atomic_doc_exists():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md DAL_ONLY Scope."""
    assert DAL_ATOMIC_DOC.exists()


def test_dal_only_allowed_atomic_slots():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md DAL_ONLY Scope."""
    content = DAL_ATOMIC_DOC.read_text(encoding="utf-8")
    assert "CarrierIdentitySlot" in content
    assert "HarakaFunctionSlot" in content
    assert "SurfaceSkeletonCandidate" in content
    assert "BridgeRequiredMarker" in content


def test_dal_only_forbidden_form_and_meaning_entities():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md DAL_ONLY Scope."""
    content = DAL_ATOMIC_DOC.read_text(encoding="utf-8")
    section = get_section(content, "## DAL_ONLY Scope", "## ")
    assert "Forbidden in DAL_ONLY:" in section
    assert "RootFormCandidate" in section
    assert "ToolFormCandidate" in section
    assert "LexicalMeaning" in section
    assert "Isnad" in section
    assert "Hukm" in section


def test_dal_atomic_rules_prohibit_premature_inference():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md Central Atomic Laws."""
    content = DAL_ATOMIC_DOC.read_text(encoding="utf-8")
    assert "No meaning from haraka." in content
    assert "No i'rab from haraka before relation." in content
    assert "No hukm from i'rab before ifadeh." in content


def test_dal_atomic_forbidden_shortcuts_are_explicit():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md Forbidden Shortcut Claims."""
    content = DAL_ATOMIC_DOC.read_text(encoding="utf-8")
    assert "`C=1 => tool`" in content
    assert "`C=3 => root`" in content
    assert "`CVCVCV => verb`" in content
    assert "`fatha => accusative`" in content
    assert "`damma => nominative`" in content
