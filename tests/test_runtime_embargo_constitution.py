"""Runtime embargo guardrails for PR #38 (docs + tests only)."""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
EMBARGO_DOC = REPO_ROOT / "docs" / "12_RUNTIME_EMBARGO_CONSTITUTION.md"
L1_SOURCE = REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1"

FORBIDDEN_FILES = [
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "binding_kernel.py",
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "decision_engine.py",
    REPO_ROOT / "coverage_matrix_v0.1.yaml",
]

FORBIDDEN_SOURCE_PATTERNS = [
    "Rank.CERTIFICATE",
    "Rank.REJECTED",
    "domain_proved: bool",
    "identity_preserved: bool",
    "gate_passed: bool",
    "computed_verdict:",
    "mrk_defaults:",
]


def test_runtime_embargo_document_exists_and_declares_authority():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5."""
    assert EMBARGO_DOC.exists()
    content = EMBARGO_DOC.read_text(encoding="utf-8")
    assert "Runtime remains embargoed" in content
    assert "binding_kernel.py is forbidden before embargo lift." in content
    assert "coverage_matrix_v0.1.yaml is forbidden before computed coverage schema." in content


def test_runtime_embargo_forbidden_files_absent():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    for forbidden in FORBIDDEN_FILES:
        assert not forbidden.exists(), f"Forbidden pre-embargo artifact exists: {forbidden}"


def test_runtime_embargo_forbidden_tokens_absent_in_l1_source_only():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule (PR #38)."""
    for path in L1_SOURCE.glob("*.py"):
        content = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_SOURCE_PATTERNS:
            assert pattern not in content, f"Forbidden token '{pattern}' found in {path}"
