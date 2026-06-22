"""
L1 closure declaration gate for L2 opening.

Authority:
- docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
- docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01
"""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
L1_CLOSURE_DOC = REPO_ROOT / "docs" / "L1_CLOSURE_DECLARATION.md"
L2_DIR = REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L2"


def test_l1_closure_declaration_document_exists_before_any_l2_opening():
    """trace_ref: docs/03_L2_LOGICAL_BOUNDARY.md BL-L2-01."""
    assert L1_CLOSURE_DOC.exists(), (
        "L2 cannot be opened without docs/L1_CLOSURE_DECLARATION.md"
    )


def test_l2_remains_locked_while_l1_closure_is_not_formally_closed():
    """trace_ref: docs/L1_CLOSURE_DECLARATION.md Closure Gate to L2."""
    content = L1_CLOSURE_DOC.read_text(encoding="utf-8")
    assert "not yet formally closed" in content.lower()

    production_files = [f for f in L2_DIR.glob("*.py") if f.name != "__init__.py"]
    assert production_files == [], (
        "L2 production code is forbidden while L1 closure is pending: "
        f"{[f.name for f in production_files]}"
    )
