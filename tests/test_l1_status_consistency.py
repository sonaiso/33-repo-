"""
PR-A status consistency tests for L0/L1 documentation.

Authority:
- docs/L0_CLOSURE_DECLARATION.md
- docs/15_PROJECT_ROADMAP.md
- docs/02_L1_META_LANGUAGE_BOUNDARY.md
"""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
README = REPO_ROOT / "README.md"
L1_BOUNDARY_DOC = REPO_ROOT / "docs" / "02_L1_META_LANGUAGE_BOUNDARY.md"
L0_CLOSURE_DOC = REPO_ROOT / "docs" / "L0_CLOSURE_DECLARATION.md"
CLAUDE_DOC = REPO_ROOT / "CLAUDE.md"


def test_l0_closed_and_l1_open_authority_exists():
    content = L0_CLOSURE_DOC.read_text(encoding="utf-8")
    assert "formally closed" in content.lower()
    assert "L1" in content
    assert "authorized" in content.lower() or "open" in content.lower()


def test_l1_boundary_document_declares_open_state():
    content = L1_BOUNDARY_DOC.read_text(encoding="utf-8")
    assert "**OPEN**" in content
    assert "PR-10" in content
    assert "PR-13" in content


def test_b_boundaries_are_internal_to_l1_only():
    content = L1_BOUNDARY_DOC.read_text(encoding="utf-8")
    assert "B0–B9" in content
    assert "internal" in content.lower()
    assert "not" in content.lower()
    assert "L0 → L1 → L2 → L3" in content


def test_readme_matches_open_l1_status():
    content = README.read_text(encoding="utf-8")
    assert "L1" in content
    assert "Open" in content
    assert "PR-9" in content
    assert "B0–B9" in content


def test_claude_md_matches_current_phase():
    content = CLAUDE_DOC.read_text(encoding="utf-8")
    assert "L0 Closed" in content
    assert "L1 Open" in content
    assert "L2/L3 Locked" in content
