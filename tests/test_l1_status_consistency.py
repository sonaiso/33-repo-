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
L1_CLOSURE_DOC = REPO_ROOT / "docs" / "L1_CLOSURE_DECLARATION.md"
CLAUDE_DOC = REPO_ROOT / "CLAUDE.md"


def test_l0_closed_and_l1_open_authority_exists():
    """trace_ref: docs/L0_CLOSURE_DECLARATION.md §Declaration."""
    content = L0_CLOSURE_DOC.read_text(encoding="utf-8")
    assert "formally closed" in content.lower()
    assert "is now authorized to begin" in content


def test_l1_boundary_document_declares_formally_closed_status():
    """trace_ref: docs/02_L1_META_LANGUAGE_BOUNDARY.md §Status + docs/L1_CLOSURE_DECLARATION.md."""
    content = L1_BOUNDARY_DOC.read_text(encoding="utf-8")
    assert "**FORMALLY CLOSED**" in content
    assert "PR #43" in content

    closure = L1_CLOSURE_DOC.read_text(encoding="utf-8")
    assert "Current status: FORMALLY CLOSED" in closure


def test_b_boundaries_are_internal_to_l1_only():
    """trace_ref: docs/02_L1_META_LANGUAGE_BOUNDARY.md §Structural Clarification."""
    content = L1_BOUNDARY_DOC.read_text(encoding="utf-8")
    assert "B0–B9" in content
    assert "internal" in content.lower()
    assert "not replacement layers" in content.lower()
    assert "L0 → L1 → L2 → L3" in content


def test_readme_matches_formally_closed_l1_status():
    """trace_ref: README.md Layer status table + next-step note."""
    content = README.read_text(encoding="utf-8")
    assert "L1" in content
    assert "✅ Formally Closed" in content
    assert "docs/L1_CLOSURE_DECLARATION.md" in content
    assert "B0–B9" in content


def test_claude_md_matches_current_phase():
    """trace_ref: CLAUDE.md §Layer Order / current phase."""
    content = CLAUDE_DOC.read_text(encoding="utf-8")
    assert "L0 Closed" in content
    assert "L1 Formally Closed" in content
    assert "L2/L3 Locked" in content
