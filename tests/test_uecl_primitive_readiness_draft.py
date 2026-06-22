"""Regression checks for the UECL primitive-readiness L1 draft."""
from pathlib import Path

from tests.markdown_sections import get_section


REPO_ROOT = Path(__file__).parent.parent
DRAFT_DOC = REPO_ROOT / "docs" / "UECL_PRIMITIVE_READINESS_DRAFT.md"
# trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md embargo before release claims.
FORBIDDEN_RELEASE_FINAL_PHRASES = (
    "Release v1.0",
    "Final Executable Declaration",
    "SupremeIdentityCourt",
    "pip install uecl-core",
)



def test_uecl_primitive_readiness_draft_exists() -> None:
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1."""
    assert DRAFT_DOC.exists()
    assert DRAFT_DOC.read_text(encoding="utf-8").strip()



def test_uecl_draft_declares_l1_provisional_scope_only() -> None:
    """trace_ref: docs/02_L1_META_LANGUAGE_BOUNDARY.md L1 internal scope."""
    content = DRAFT_DOC.read_text(encoding="utf-8")
    assert "provisional L1 draft contract" in content
    opened_scope = get_section(content, "## Opened Scope (L1 only)", "## ")
    assert "- Trace" in opened_scope
    assert "- SignifierDomain" in opened_scope
    assert "- ClosureCertificate" in opened_scope
    assert "closed" in opened_scope
    assert "provisional" in opened_scope
    assert "blocked" in opened_scope
    assert "LogicalComparison" not in content
    assert "MaqoolVerdict" not in content
    assert "HukmCandidate" not in content



def test_uecl_draft_documents_forbidden_l2_l3_terms() -> None:
    """trace_ref: docs/15_PROJECT_ROADMAP.md no premature L2/L3 opening."""
    content = DRAFT_DOC.read_text(encoding="utf-8")
    assert "- qiyas" in content
    assert "- illah" in content
    assert "- ifadah" in content
    assert "- hukm" in content
    assert "- reality/tanzil adjudication" in content



def test_uecl_draft_blocks_release_and_final_claims() -> None:
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md embargo before release claims."""
    content = DRAFT_DOC.read_text(encoding="utf-8")
    for phrase in FORBIDDEN_RELEASE_FINAL_PHRASES:
        assert phrase not in content
    assert "No final certificate or final verdict is produced at this stage." in content
