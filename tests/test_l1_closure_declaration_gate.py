"""
L1 closure declaration gate for L2 opening.

Authority:
- docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
- docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01

trace_ref: docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01
"""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
L1_CLOSURE_DOC = REPO_ROOT / "docs" / "L1_CLOSURE_DECLARATION.md"
L2_DIR = REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L2"
L1_STATUS_FORMAL_MARKER = "Current status: FORMALLY CLOSED"
L1_STATUS_CANDIDATE_MARKER = "L1_CLOSURE_CANDIDATE"
REQUIRED_VERIFICATION_MARKERS = (
    "`pytest tests/` → **PASS**",
    "`pytest tests/test_kpi_indicators.py -v` → **PASS**",
    "`python -m ci.constitutional_guard --source-dir src` → **PASS**",
)


def test_l1_closure_declaration_exists():
    """trace_ref: docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01."""
    assert L1_CLOSURE_DOC.exists(), (
        "L2 cannot be opened without docs/L1_CLOSURE_DECLARATION.md"
    )


def test_l1_declaration_has_valid_status_marker():
    """trace_ref: docs/L1_CLOSURE_DECLARATION.md Closure Gate to L2."""
    content = L1_CLOSURE_DOC.read_text(encoding="utf-8")
    casefold_content = content.casefold()
    has_formal = L1_STATUS_FORMAL_MARKER.casefold() in casefold_content
    has_candidate = L1_STATUS_CANDIDATE_MARKER.casefold() in casefold_content

    assert has_formal or has_candidate, (
        "L1 declaration must expose either FORMALLY CLOSED or "
        "L1_CLOSURE_CANDIDATE status marker"
    )

    if has_formal:
        for marker in REQUIRED_VERIFICATION_MARKERS:
            assert marker in content
    else:
        assert "Residuals / Blockers" in content
        assert "L1_CLOSURE_CANDIDATE" in content
        assert any(
            marker not in content for marker in REQUIRED_VERIFICATION_MARKERS
        ), "Candidate status must have at least one missing verification marker"


def test_l2_remains_locked_until_explicit_l2_opening_authorization():
    """trace_ref: docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01."""
    content = L1_CLOSURE_DOC.read_text(encoding="utf-8").lower()
    assert "l2 remains locked" in content

    production_files = [f for f in L2_DIR.glob("*.py") if f.name != "__init__.py"]
    assert production_files == [], (
        "L2 production code is forbidden until explicit L2 opening authorization: "
        f"{[f.name for f in production_files]}"
    )
