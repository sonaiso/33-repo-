"""Runtime Embargo Readiness Ledger guardrails for PR #65 (docs + tests only)."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
LEDGER_DOC = REPO_ROOT / "docs" / "17_RUNTIME_EMBARGO_READINESS_LEDGER.md"

REQUIRED_PHRASES = [
    "Runtime Embargo remains active.",
    "Kernel is not authorized.",
    "Decision engine is not authorized.",
    "Coverage matrix runtime is not authorized.",
    "Anti-pattern guard green",
    "| Anti-pattern guard green | DONE |",
    "| TraceStep identity ProofObject-backed | PARTIAL |",
    "explicit bool only",
    "| Runtime kernel allowed | NOT AUTHORIZED |",
    "| decision_engine.py allowed | NOT AUTHORIZED |",
    "| coverage_matrix_v0.1.yaml allowed | NOT AUTHORIZED |",
]

FORBIDDEN_PHRASES = [
    "embargo lifted",
]


def test_runtime_embargo_readiness_ledger_exists():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    assert LEDGER_DOC.exists(), "Missing runtime embargo readiness ledger document"


def test_runtime_embargo_readiness_ledger_has_required_claims():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    content = LEDGER_DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_PHRASES:
        assert phrase in content, f"Missing required readiness phrase: {phrase}"


def test_runtime_embargo_readiness_ledger_does_not_claim_embargo_lifted():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = LEDGER_DOC.read_text(encoding="utf-8").lower()
    for phrase in FORBIDDEN_PHRASES:
        assert phrase not in content, f"Forbidden phrase found in readiness ledger: {phrase}"
