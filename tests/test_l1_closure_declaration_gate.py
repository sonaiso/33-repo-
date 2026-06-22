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
L1_STATUS_FORMAL_MARKER = "current status: formally closed"
L1_STATUS_CANDIDATE_MARKER = "l1_closure_candidate"


def test_l1_closure_declaration_exists():
    """trace_ref: docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01."""
    assert L1_CLOSURE_DOC.exists(), (
        "L2 cannot be opened without docs/L1_CLOSURE_DECLARATION.md"
    )


def test_l1_declaration_uses_test_outcome_status():
    """trace_ref: docs/L1_CLOSURE_DECLARATION.md Closure Gate to L2."""
    content = L1_CLOSURE_DOC.read_text(encoding="utf-8")
    lowered = content.lower()
    has_formal = L1_STATUS_FORMAL_MARKER in lowered
    has_candidate = L1_STATUS_CANDIDATE_MARKER in lowered

    assert has_formal or has_candidate, (
        "L1 declaration must expose either FORMALLY CLOSED or "
        "L1_CLOSURE_CANDIDATE status marker"
    )

    if has_formal:
        assert "`pytest tests/` → **PASS**" in content
        assert "`pytest tests/test_kpi_indicators.py -v` → **PASS**" in content
        assert (
            "`python -m ci.constitutional_guard --source-dir src` → **PASS**"
            in content
        )
    else:
        assert "Residuals / Blockers" in content
        assert "L1_CLOSURE_CANDIDATE" in content


def test_l2_remains_locked_even_after_l1_declaration():
    """trace_ref: docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01."""
    content = L1_CLOSURE_DOC.read_text(encoding="utf-8").lower()
    assert "l2 remains locked" in content

    production_files = [f for f in L2_DIR.glob("*.py") if f.name != "__init__.py"]
    assert production_files == [], (
        "L2 production code is forbidden until explicit L2 opening authorization: "
        f"{[f.name for f in production_files]}"
    )
